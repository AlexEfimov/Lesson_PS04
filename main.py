from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

import time


def get_user_input(prompt):
    return input(prompt).strip()


def navigate_to_search(browser, query):
    search_box = browser.find_element(By.ID, "searchInput")
    search_box.clear()
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)
    time.sleep(2)  # Wait for the page to load
    # a = browser.find_element(By.LINK_TEXT, query)
    # a.click()
    # first_result = browser.find_element(By.CSS_SELECTOR, "a")
    # first_result.click()
    first_result = browser.find_element(By.CSS_SELECTOR, "div.mw-search-result-heading > a")
    first_result.click()




def list_paragraphs(browser):
    paragraphs = browser.find_elements(By.TAG_NAME, "p")
    for paragraph in paragraphs:
        print(paragraph.text)
        input()
    #for idx, para in enumerate(paragraphs):
    #    print(f"Paragraph {idx + 1}:\n{para.text}\n")
    return paragraphs


def list_internal_links(browser):
    links = browser.find_elements(By.CSS_SELECTOR, "div.mw-parser-output > p a[href^='/wiki/']")
    for idx, link in enumerate(links):
        print(f"Link {idx + 1}: {link.text} ({link.get_attribute('href')})")
    return links


def main():

    browser = webdriver.Firefox()

    try:
        browser.get(
            "https://ru.wikipedia.org/wiki/%D0%97%D0%B0%D0%B3%D0%BB%D0%B0%D0%B2%D0%BD%D0%B0%D1%8F_%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0")
        time.sleep(2)  # Wait for the page to load

        initial_query = get_user_input("Введите ваш запрос для поиска на Википедии: ")
        navigate_to_search(browser, initial_query)

        while True:
            print("\nВыберите действие:")
            print("1. Листать параграфы текущей статьи")
            print("2. Перейти на одну из связанных страниц")
            print("3. Выйти из программы")

            choice = get_user_input("Ваш выбор (1, 2, 3): ")

            if choice == "1":
                list_paragraphs(browser)
            elif choice == "2":
                links = list_internal_links(browser)
                if not links:
                    print("Связанные страницы не найдены.")
                    continue

                link_choice = get_user_input("Введите номер ссылки для перехода: ")
                try:
                    link_index = int(link_choice) - 1
                    if 0 <= link_index < len(links):
                        links[link_index].click()
                        time.sleep(2)  # Wait for the page to load
                    else:
                        print("Неверный номер ссылки.")
                except ValueError:
                    print("Пожалуйста, введите номер ссылки.")
            elif choice == "3":
                break
            else:
                print("Неверный выбор. Попробуйте снова.")

    finally:
        browser.quit()


if __name__ == "__main__":
    main()