import time, subprocess, os.path, re, multiprocessing, threading
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class SG:
	driver = None
	dispatcher_thread = None
	argument_lists = []
	stop_dispatching = False
	
	def __init__(self, exec_dir, username, password, dir, process_limit, urls, type, time_period):
		SG.dispatcher_thread = threading.Thread(target=self.__dispatch)
		
		self.username = username
		self.password = password
		self.root_url = "https://www.suicidegirls.com/"
		self.dir = dir
		self.exec_dir = exec_dir
		self.process_limit = process_limit
		self.urls = []
		self.__type = type
		self.process_limit = process_limit
		self.time_period = time_period
		self.girls_completed = 0
		self.sets_completed = 0
		
		if type in ["girl", "hopeful"]:
			for url in urls:
				self.urls.append(self.__build_url(url))
				print(self.__build_url(url))
		else:
			self.urls = urls
			
		SG.dispatcher_thread.start()
		
	def __dispatch(self):
		print("Beginning dispatcher thread...")
		while not SG.stop_dispatching or len(SG.argument_lists) != 0:
			if len(SG.argument_lists) != 0:
				print("Argument list found! Dispatching...")
				argument_list = SG.argument_lists.pop(0)

				pool = multiprocessing.Pool(self.process_limit)
				#driver = SG.driver
				
				#SG.driver = None
				
				pool.map(self.download_image, argument_list)
				
				# Girls: Riae (36), Fishball (28), Vandoll (7)
				# Total photosets: 71
				# Processes: 8
				# map: 00:24:37
				# map_async: 00:12:33
				
				#SG.driver = driver
		print("Exiting dispatcher thread...")
		
	def startup(self):
		SG.driver = webdriver.Chrome(executable_path="dependencies/chromedriver.exe")
		SG.driver.maximize_window()
		SG.driver.implicitly_wait(5)
		SG.driver.get(self.root_url)
		self.__login()
	
	def shutdown(self):
		SG.driver.quit()
	
	def __login(self):
		login_button_xpath = "//a[@class='login button' or @class='button login']"
		login_form_submit_xpath = "//button[@type='submit' and text()='Login']"
		username_box_xpath = "//input[@name='username']"
		password_box_xpath = "//input[@name='password']"
		
		SG.driver.find_element_by_xpath(login_button_xpath).click()
		SG.driver.find_element_by_xpath(username_box_xpath).send_keys(self.username)
		SG.driver.find_element_by_xpath(password_box_xpath).send_keys(self.password)
		SG.driver.find_element_by_xpath(login_form_submit_xpath).click()

		time.sleep(5)
		
		flag = False;
		while True:
			try:
				image_select = SG.driver.find_element_by_xpath("//iframe[@title='recaptcha challenge']")
				if not flag:
					print("Found a captcha!")
					flag = True
			except:
				break;
		print("No captcha found!")

	def rip(self):
		for url in self.urls:
			SG.driver.get(url)
			if self.__type == "girl":
				print("Single girl")
				self.__rip_girl()
			elif self.__type == "girls":
				print("All Suicide Girls")
				self.__rip_all_girls()
			elif self.__type == "hopefuls":
				print("All hopefuls")
				self.__rip_all_hopefuls()
			elif self.__type == "sotds":
				print("All sets of the day")
				self.__rip_all_sets_of_the_day()
			elif self.__type == "set":
				print("Single set")
				self.__rip_set()
			elif self.__type == "all":
				print("All!")
				self.__rip_all_photos()
		
		SG.stop_dispatching = True
		SG.dispatcher_thread.join()
		
		print("Rip completed.")
		print("Total girls/hopefuls ripped: " + str(self.girls_completed))
		print("Total sets ripped: " + str(self.sets_completed))
		
	def __rip_all_photos(self):
		SG.driver.get(self.urls[0])
		self.__type = "hopefuls"
		self.__rip_all_hopefuls()
		SG.driver.get(self.urls[0])
		self.__type = "girls"
		self.__rip_all_girls()
		SG.driver.get(self.urls[0])
		self.__type = "sotds"
		self.__rip_all_sets_of_the_day()
		
	def __rip_all_girls(self):
		suicide_girls_xpath = "//li[@class='dropdown'][1]//ul/li/a[text() = 'SuicideGirls']"
		
		self.__rip_all(suicide_girls_xpath)
		
	def __rip_all_hopefuls(self):
		hopefuls_xpath = "//li[@class='dropdown'][1]//ul/li/a[text() = 'Hopefuls']"
		
		self.__rip_all(hopefuls_xpath)
		
	def __rip_all_sets_of_the_day(self):
		sotds_xpath = "//li[@class='dropdown'][1]//ul/li/a[text() = 'Sets Of The Day']"
		
		self.__rip_all(sotds_xpath)
		
	def __rip_all(self, type_xpath):
		time_period_xpath = "//li[@class='dropdown'][3]//ul/li/a[text() = '" + self.time_period + "']"
		girl_name_xpath = "//article/header//h2/a"
		load_more_xpath = "//a[@id='load-more']"
		
		choice = SG.driver.find_element_by_xpath(type_xpath)
		SG.driver.get(choice.get_attribute("href"))
		
		choice = SG.driver.find_element_by_xpath(time_period_xpath)
		SG.driver.get(choice.get_attribute("href"))
		
		girls = []
		
		iteration = 0
		while True:
			iteration += 1
			names = SG.driver.find_elements_by_xpath(girl_name_xpath)
			for name in names:
				girls.append(name.text)
			if iteration > 1:
				SG.driver.execute_script("for(i=0;i<24;i++) {e = document.evaluate(\"//article[1]\", document.documentElement); e = e.iterateNext(); if (e == null) {break;}e.parentNode.removeChild(e);}")
				time.sleep(2)
			lmb = SG.driver.find_elements_by_xpath(load_more_xpath)
			if len(lmb) > 0 and lmb[0].is_displayed():
				lmb[0].click()
				time.sleep(10)
			else:
				break

		girls = list(set(girls))
		
		for girl in sorted(girls):
			url = self.__build_url(girl)
			SG.driver.get(url)
			self.__rip_girl()
			
		
	def __rip_girl(self):
		load_more_xpath = "//a[@id='load-more']"
		photos_xpath = "//div[@id='content-container']//a[text()='Photos']"
		photosets_xpath = "//div[@id='content-container']//a[text()='Photosets']"
		set_title_xpath = "//article/header//h2/a"
		
		url = SG.driver.find_element_by_xpath(photos_xpath).get_attribute("href")
		SG.driver.get(url)
		url = SG.driver.find_element_by_xpath(photosets_xpath).get_attribute("href")
		SG.driver.get(url)
	
		set_links = []
		
		iteration = 0
		while True:
			iteration += 1
			titles = SG.driver.find_elements_by_xpath(set_title_xpath)
			for title in titles:
				set_links.append(title.get_attribute("href"))
			if iteration > 1:
				SG.driver.execute_script("for(i=0;i<9;i++) {e = document.evaluate(\"//article[1]\", document.documentElement); e = e.iterateNext(); if (e == null) {break;}e.parentNode.removeChild(e);}")
				time.sleep(2)
			lmb = SG.driver.find_elements_by_xpath(load_more_xpath)
			if len(lmb) > 0 and lmb[0].is_displayed():
				lmb[0].click()
				time.sleep(10)
			else:
				break
			
		set_links = list(set(set_links))
		
		for link in set_links:
			SG.driver.get(link)
			self.__rip_set()
			
		self.girls_completed += 1
		
	def __rip_set(self):
		girl_xpath = "//h1/a"
		title_xpath = "//header[@class='header']/div[@class='top-bar']/h2[@class='title']"
		full_image_button_xpath = "//a[@id='button-view_full_size']"
		full_image_url_xpath = "//div[@data-image_url]"
		
		girl = SG.driver.find_element_by_xpath(girl_xpath).text
		title = SG.driver.find_element_by_xpath(title_xpath).text
		
		dir_name = os.path.join("Suicide Girls", girl.title(), title.title())
		dir_name = re.subn("[<>:\"/\|?*]", "", dir_name)[0]
		dir_name = re.subn("\\.{3,}", "…", dir_name)[0]
		dir_name = os.path.join(self.dir, dir_name)
		
		check = False
		if os.path.exists(dir_name):
			check = True
		
		SG.driver.find_element_by_xpath(full_image_button_xpath).click()
		time.sleep(5)
		
		images = SG.driver.find_elements_by_xpath(full_image_url_xpath)
		
		image_urls = []
		for i in range(0, len(images)):
			url = images[i].get_attribute("data-image_url")
			ext = url[url.rindex("."):]
			file_name = "Suicide Girls - " + girl.title() + " - " + title.title() + " - Img" + str(i + 1).zfill(3) + ext
			file_name = re.subn("[<>:\"/\|?*]", "", file_name)[0]
			file_name = re.subn("\\.{3,}", "…", file_name)[0]
			
			if not os.path.exists(os.path.join(dir_name, file_name)):
				image_urls.append(url)
			else:
				print(girl.title() + "/" + title.title() + " Img" + str(i).zfill(3) + " already exists, skipping...")
			
		self.__download_and_save_set(image_urls, girl, title)
		
		self.sets_completed += 1
		
	def __download_and_save_set(self, urls, girl, title):
		aria_path = os.path.join(self.exec_dir, "dependencies", "aria2", "aria2c.exe")
		error_strings = []
		
		dir_name = os.path.join("Suicide Girls", girl.title(), title.title())
		dir_name = re.subn("[<>:\"/\|?*]", "", dir_name)[0]
		dir_name = re.subn("\\.{3,}", "…", dir_name)[0]
		dir_name = os.path.join(self.dir, dir_name)

		with multiprocessing.Pool(8) as pool:
			args = []
			for i in range (0, len(urls)):
				command = [aria_path, "-d", dir_name, "-o"]

				ext = urls[i][urls[i].rindex("."):]
				file_name = "Suicide Girls - " + girl.title() + " - " + title.title() + " - Img" + str(i + 1).zfill(3) + ext
				file_name = re.subn("[<>:\"/\|?*]", "", file_name)[0]
				file_name = re.subn("\\.{3,}", "…", file_name)[0]

				if os.path.exists(dir_name + file_name):
					continue

				command.append(file_name)
				command.append(urls[i])
				
				args.append((error_strings, command, str(i + 1), urls[i], girl, title))
			
			SG.argument_lists.append(args)
		
		if len(error_strings) > 0:
			f = open(os.path.join(dir_name, "errors.txt", "w"))
			f.write("\n".join(sorted(error_strings)))
			f.close()
		
	def __build_url(self, name):
		if self.__type in ["girl", "girls", "sotds"]:
			return "https://www.suicidegirls.com/girls/" + name
		elif self.__type in ["hopeful", "hopefuls"]:
			return "https://www.suicidegirls.com/members/" + name
	
	def download_image(self, args):
		process = subprocess.run(args[1])
		if process.returncode != 0:
			args[0].append("\tImage " + args[2] + " failed; URL: " + args[3])
		print(args[4].title() + "/" + args[5].title() + " #" + args[2] + " complete")
		
	def start_processes(async_result):
		async_result.get()
		
def print_warning():
	print("This file is meant to be imported by other Python files, not run directly. Exiting now.")

if __name__ == "__main__":
	print_warning()
