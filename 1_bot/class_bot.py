from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from auth_data import username, password
from direct_users_list import direct_users_list
from selenium.common.exceptions import NoSuchElementException
# импортируем модули time and random to create pause52
import time
import random
import requests
import os


class InstagramBot():

    def __init__(self, username, password):

        self.username = username
        self.password = password
        self.browser = webdriver.Chrome('../chromedriver/chromedriver.exe')

    def close_browser(self):

        self.browser.close()
        self.browser.quit()

    def login(self):

        """создаем экземпляр класса гугл хром и передаем ему
           в качестве параметра путь до драйвера"""
        browser = self.browser
        browser.get('https://instagram.com')
        # установим рандомную паузу от 3-до 5
        time.sleep(random.randrange(3, 5))
        # находим поле ввода юзернейма
        username_input = browser.find_element_by_name('username')
        # очищаем на всякий случай
        username_input.clear()
        # вводим наш юзернэйм
        username_input.send_keys(username)
        # 2 sec delay
        time.sleep(2)
        # находим поле ввода пароля
        password_input = browser.find_element_by_name('password')
        # очищаем на всякий случай
        password_input.clear()
        # вводим наш пароль
        password_input.send_keys(password)
        # нажимаем на кнопку ввода
        password_input.send_keys(Keys.ENTER)
        time.sleep(20)

    def like_photo_by_hastag(self, hashtag):

        browser = self.browser
        browser.get(f'https://www.instagram.com/explore/tags/{hashtag}/')
        time.sleep(5)
        # имитируем скрол страницы
        for i in range(1, 4):  # 4 скрола
            browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            time.sleep(random.randrange(3, 5))

        # сoбираем все ссылки со страницы
        hrefs = browser.find_elements_by_tag_name('a')
        # формируем список нужных ссылок
        posts_url = [item.get_attribute('href') for item in hrefs if "/p/" in item.get_attribute('href')]
        # print(posts_url)
        # лайкаем все посты по хэштегу
        for url in posts_url:
            try:
                browser.get(url)
                time.sleep(5)
                # в модальном окне отрабатывать это икспас не будет
                like_button = browser.find_element_by_xpath(
                    '/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[1]/span[1]/button').click()
                time.sleep(random.randrange(80, 100))
            except Exception as ex:
                print(ex)
                self.browser.close()

    # проверяем по xpath существует ли элемент на странице
    def xpath_exist(self, url):

        browser = self.browser
        try:
            browser.find_element_by_xpath(url)
            exist = True
        except NoSuchElementException:
            exist = False
        return exist

    # ставим лайк на пост по прямой ссылке

    def put_exactly_like(self, userpost):

        browser = self.browser
        browser.get(userpost)
        time.sleep(4)

        wrong_userpage = "/html/body/div[1]/section/main/div/h2"
        if self.xpath_exist(wrong_userpage):
            print('Поста не существует проверь URL')
            self.close_browser()
        else:
            print('Пост успешно найден, ставим лайк')
            time.sleep(2)

            like_button = "html/body/div[1]/section/main/div/div/article/div[3]/section[1]/span[1]/button"
            browser.find_element_by_xpath(like_button).click()
            time.sleep(2)
            print(f'Лайк на пост {userpost} успешно поставлен')
            self.close_browser()

    # метод собирает ссылки на все посты пользователя

    def get_all_posts_urls(self, userpage):
        browser = self.browser
        browser.get(userpage)
        time.sleep(4)

        wrong_userpage = "/html/body/div[1]/section/main/div/h2"
        if self.xpath_exist(wrong_userpage):
            print('Юзера не существует проверь URL')
            self.close_browser()
        else:
            print('Юзер успешно найден, ставим лайк')
            time.sleep(2)

            post_count = int(browser.find_element_by_xpath(
                '/html/body/div[1]/section/main/div/header/section/ul/li[1]/span/span').text)
            loops_count = int(post_count / 12)
            print(loops_count)
            time.sleep(2)

            posts_urls = []
            # проверка условия прокрутки страницы если мало простов то else
            if loops_count > 0:
                for i in range(0, loops_count):
                    hrefs = browser.find_elements_by_tag_name('a')
                    hrefs = [item.get_attribute('href') for item in hrefs if "/p/" in item.get_attribute('href')]

                    for href in hrefs:
                        posts_urls.append(href)

                    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(random.randrange(3, 5))
                    print(f"Итерация #{i}")
            else:
                print("прокрутка не требуется")
                hrefs = browser.find_elements_by_tag_name('a')
                hrefs = [item.get_attribute('href') for item in hrefs if "/p/" in item.get_attribute('href')]
                for href in hrefs:
                    posts_urls.append(href)
                time.sleep(random.randrange(3, 5))

            file_name = userpage.split('/')[-2]

            with open(f'{file_name}.txt', 'a', encoding='utf-8') as file:
                for post_url in posts_urls:
                    file.write(post_url + "\n")

            # избавимся от задвоения сслыок и внесем рандом
            set_posts_urls = set(posts_urls)
            set_posts_urls = list(set_posts_urls)

            with open(f'{file_name}_set.txt', 'a', encoding='utf-8') as f:
                for post_url in set_posts_urls:
                    f.write(post_url + '\n')


    def put_many_likes(self, userpage):

        browser = self.browser
        self.get_all_posts_urls(userpage)
        file_name = userpage.split('/')[-2]
        time.sleep(4)
        browser.get(userpage)
        time.sleep(4)

        # лайкаем
        with open(f'{file_name}_set.txt') as file:
            urls_list = file.readlines()

            for post_url in urls_list[:10]:
                try:
                    browser.get(post_url)
                    time.sleep(2)

                    like_button = "html/body/div[1]/section/main/div/div/article/div[3]/section[1]/span[1]/button"
                    browser.find_element_by_xpath(like_button).click()
                    # time.sleep(random.randrange(80, 100))
                    time.sleep(2)

                    print(f'Лайк на пост {post_url} успешно поставлен')
                except Exception as ex:
                    print(ex)
                    self.close_browser()

    def download_userpage_content(self, userpage):

        browser = self.browser
        self.get_all_posts_urls(userpage)
        file_name = userpage.split('/')[-2]
        time.sleep(4)
        browser.get(userpage)
        time.sleep(4)

        #создаем папку с именем пользователя
        if os.path.exists(f'{file_name}'):
            print('папка уже есть')
        else:
            os.mkdir(file_name)

        # сохраним ссылки в список
        img_and_video_src_urls = []
        with open(f'{file_name}_set.txt') as file:
            urls_list = file.readlines()

            for post_url in urls_list:
                try:
                    browser.get(post_url)
                    time.sleep(4)

                    img_src = '/html/body/div[1]/section/main/div/div[1]/article/div[2]/div/div/div[1]/img'
                    video_src = '/html/body/div[1]/section/main/div/div[1]/article/div[2]/div/div/div[1]/div/div/video'
                    post_id = post_url.split('/')[-2]
                    #если картинка есть на странице то мы забираем ссылку из атрибута src
                    if self.xpath_exist(img_src):
                        img_src_url = browser.find_element_by_xpath(img_src).get_attribute('src')
                        img_and_video_src_urls.append(img_src_url)
                        # сохраняем изображение
                        get_img = requests.get(img_src_url)
                        with open(f'{file_name}/{file_name}_{post_id}_img.jpg', 'wb') as img_file:
                            img_file.write(get_img.content)

                    elif self.xpath_exist(video_src):
                        video_src_url = browser.find_element_by_xpath(video_src).get_attribute('src')
                        img_and_video_src_urls.append(video_src_url)

                        # сохраняем видео
                        get_video = requests.get(video_src_url, stream=True)
                        with open(f'{file_name}/{file_name}_{post_id}_video.mp4', 'wb') as video_file:
                            video_file.write(get_video.content)
                            for chunk in get_video.iter_content(chunk_size=1024*1024):
                                if chunk:
                                    video_file.write(chunk)
                    else:
                        # print('что-то сломалось')
                        img_and_video_src_urls.append(f'{post_url} нет ссылки')
                    print(f'контент из поста {post_url} успешно скачан')

                except Exception as ex:
                    print(ex)
                    self.close_browser()

            self.close_browser()

        with open(f'{file_name}/{file_name}_img_and_video_src_urls.txt', 'a') as file:
            for i in img_and_video_src_urls:
                file.write(i + '\n')

        # метод подписки на всех подписчиков переданного аккаунта

    def get_all_followers(self, userpage):

        browser = self.browser
        browser.get(userpage)
        time.sleep(4)
        file_name = userpage.split("/")[-2]

        # создаём папку с именем пользователя для чистоты проекта
        if os.path.exists(f"{file_name}"):
            print(f"Папка {file_name} уже существует!")
        else:
            print(f"Создаём папку пользователя {file_name}.")
            os.mkdir(file_name)

        wrong_userpage = "/html/body/div[1]/section/main/div/h2"
        if self.xpath_exist(wrong_userpage):
            print(f"Пользователя {file_name} не существует, проверьте URL")
            self.close_browser()
        else:
            print(f"Пользователь {file_name} успешно найден, начинаем скачивать ссылки на подписчиков!")
            time.sleep(2)

            followers_button = browser.find_element_by_xpath(
                "/html/body/div[1]/section/main/div/header/section/ul/li[2]/a")
            followers_count = followers_button.text
            followers_count = int(followers_count.split(' ')[0])
            print(f"Количество подписчиков: {followers_count}")
            time.sleep(2)

            loops_count = int(followers_count / 12)
            print(f"Число итераций: {loops_count}")
            time.sleep(4)

            followers_button.click()
            time.sleep(4)

            followers_ul = browser.find_element_by_xpath("/html/body/div[5]/div/div")

            try:
                followers_urls = []
                for i in range(1, loops_count + 1):
                    browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", followers_ul)
                    time.sleep(random.randrange(2, 4))
                    print(f"Итерация #{i}")

                all_urls_div = followers_ul.find_elements_by_tag_name("li")

                for url in all_urls_div:
                    url = url.find_element_by_tag_name("a").get_attribute("href")
                    followers_urls.append(url)

                # сохраняем всех подписчиков пользователя в файл
                with open(f"{file_name}/{file_name}.txt", "a") as text_file:
                    for link in followers_urls:
                        text_file.write(link + "\n")

                with open(f"{file_name}/{file_name}.txt") as text_file:
                    users_urls = text_file.readlines()

                    for user in users_urls[0:10]:
                        try:
                            try:
                                with open(f'{file_name}/{file_name}_subscribe_list.txt',
                                          'r') as subscribe_list_file:
                                    lines = subscribe_list_file.readlines()
                                    if user in lines:
                                        print(f'Мы уже подписаны на {user}, переходим к следующему пользователю!')
                                        continue

                            except Exception as ex:
                                print('Файл со ссылками ещё не создан!')
                                # print(ex)

                            browser = self.browser
                            browser.get(user)
                            page_owner = user.split("/")[-2]

                            if self.xpath_exist("/html/body/div[1]/section/main/div/header/section/div[1]/div/a"):

                                print("Это наш профиль, уже подписан, пропускаем итерацию!")
                            elif self.xpath_exist(
                                    "/html/body/div[1]/section/main/div/header/section/div[1]/div[2]/div/span/span[1]/button/div/span"):
                                print(f"Уже подписаны, на {page_owner} пропускаем итерацию!")
                            else:
                                time.sleep(random.randrange(4, 8))

                                if self.xpath_exist(
                                        "/html/body/div[1]/section/main/div/div/article/div[1]/div/h2"):
                                    try:
                                        follow_button = browser.find_element_by_xpath(
                                            "/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/button").click()
                                        print(f'Запросили подписку на пользователя {page_owner}. Закрытый аккаунт!')
                                    except Exception as ex:
                                        print(ex)
                                else:
                                    try:
                                        if self.xpath_exist(
                                                "/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/button"):
                                            follow_button = browser.find_element_by_xpath(
                                                "/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/button").click()
                                            print(f'Подписались на пользователя {page_owner}. Открытый аккаунт!')
                                        else:
                                            follow_button = browser.find_element_by_xpath(
                                                "/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div/div/span/span[1]/button").click()
                                            print(f'Подписались на пользователя {page_owner}. Открытый аккаунт!')
                                    except Exception as ex:
                                        print(ex)

                                # записываем данные в файл для ссылок всех подписок, если файла нет, создаём, если есть - дополняем
                                with open(f'{file_name}/{file_name}_subscribe_list.txt',
                                          'a') as subscribe_list_file:
                                    subscribe_list_file.write(user)

                                time.sleep(random.randrange(7, 15))

                        except Exception as ex:
                            print(ex)
                            self.close_browser()

            except Exception as ex:
                print(ex)
                self.close_browser()

        self.close_browser()


    # метод для отправки сообщения в директ
    def send_direct_message(self, username='', message=''):

        browser = self.browser
        time.sleep(random.randrange(2, 4))
        direct_button_message = '/html/body/div[1]/section/nav/div[2]/div/div/div[3]/div/div[2]/a'

        if not self.xpath_exist(direct_button_message):
            print('кнопка отправки сообщения не найдена')
            self.close_browser()
        else:
            print('отправляем сообщение...')
            direct_message = browser.find_element_by_xpath(direct_button_message).click()
            time.sleep(random.randrange(2, 4))

        # отключаем всплывающее окно
        if self.xpath_exist('/html/body/div[5]/div'):
            browser.find_element_by_xpath('/html/body/div[5]/div/div/div/div[3]/button[2]').click()
        time.sleep(random.randrange(2, 4))

        send_message_button = browser.find_element_by_xpath('/html/body/div[1]/section/div/div[2]/div/div/div[2]/div/div[3]/div/button').click()
        time.sleep(random.randrange(2, 4))

        # вводим получателя
        to_input = browser.find_element_by_xpath('/html/body/div[5]/div/div/div[2]/div[1]/div/div[2]/input')
        to_input.send_keys(username)
        time.sleep(random.randrange(2, 4))

        # выбираем получателя из списка
        users_list = browser.find_element_by_xpath('/html/body/div[5]/div/div/div[2]/div[2]').find_element_by_tag_name('button').click()
        time.sleep(random.randrange(2, 4))

        next_button = browser.find_element_by_xpath('/html/body/div[5]/div/div/div[1]/div/div[2]/div/button').click()
        time.sleep(random.randrange(2, 4))

        text_message_area = browser.find_element_by_xpath('/html/body/div[1]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[2]/textarea')
        text_message_area.clear()
        text_message_area.send_keys(message)
        time.sleep(random.randrange(2, 4))
        text_message_area.send_keys(Keys.ENTER)
        print(f'Сообщение для {username} успешно отправлено')

        self.close_browser()



    # метод массовой рассылки сообщений в директ
    def masiv_sending_messages(self, usernames='', message='', img_path=''):

        browser = self.browser
        time.sleep(random.randrange(2, 4))
        direct_button_message = '/html/body/div[1]/section/nav/div[2]/div/div/div[3]/div/div[2]/a'

        if not self.xpath_exist(direct_button_message):
            print('кнопка отправки сообщения не найдена')
            self.close_browser()
        else:
            print('отправляем сообщение...')
            direct_message = browser.find_element_by_xpath(direct_button_message).click()
            time.sleep(random.randrange(2, 4))

        # отключаем всплывающее окно
        if self.xpath_exist('/html/body/div[5]/div'):
            browser.find_element_by_xpath('/html/body/div[5]/div/div/div/div[3]/button[2]').click()
        time.sleep(random.randrange(2, 4))

        send_message_button = browser.find_element_by_xpath(
            '/html/body/div[1]/section/div/div[2]/div/div/div[2]/div/div[3]/div/button').click()
        time.sleep(random.randrange(2, 4))
        # отправка сообщений нескольким пользователям
        for user in usernames:
            # вводим получателя
            to_input = browser.find_element_by_xpath('/html/body/div[5]/div/div/div[2]/div[1]/div/div[2]/input')
            to_input.send_keys(user)
            time.sleep(random.randrange(2, 4))

            # выбираем получателя из списка
            users_list = browser.find_element_by_xpath('/html/body/div[5]/div/div/div[2]/div[2]').find_element_by_tag_name('button').click()
            time.sleep(random.randrange(2, 4))

        next_button = browser.find_element_by_xpath('/html/body/div[5]/div/div/div[1]/div/div[2]/div/button').click()
        time.sleep(random.randrange(2, 4))

        # отправка текстового сообщения
        if message:
            text_message_area = browser.find_element_by_xpath(
                '/html/body/div[1]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[2]/textarea')
            text_message_area.clear()
            text_message_area.send_keys(message)
            time.sleep(random.randrange(2, 4))
            text_message_area.send_keys(Keys.ENTER)
            print(f'Сообщение для {username} успешно отправлено')
            time.sleep(random.randrange(2, 4))

        # отправка изображения
        if img_path:
            send_message_input = browser.find_element_by_xpath('/html/body/div[1]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/form/input')
            send_message_input.send_keys(img_path)
            print(f'изображение для {usernames} успешно отправлено')
            time.sleep(random.randrange(2, 4))


        self.close_browser()



my_bot = InstagramBot(username, password)
my_bot.login()
# my_bot.get_all_followers('https://www.instagram.com/mgelatta/')
# my_bot.send_direct_message('sviteribuben', 'Hi')
my_bot.masiv_sending_messages(direct_users_list, "Hi, i'm testing my bot) Don't worry", "C:/Users/zvuk/PycharmProjects/instabot/1_bot/ph4.jpg")
# my_bot.download_userpage_content('https://www.instagram.com/elayes.lb/')
# my_bot.put_exactly_like('https://www.instagram.com/p/B9j0VnRoDOJ/')
# my_bot.like_photo_by_hastag('data')
