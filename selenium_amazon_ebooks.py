import time

from selenium.webdriver import Firefox
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

example_url = "https://www.amazon.co.uk/hz/mycd/digital-console/contentlist/booksAll/dateDsc/"
popup_key = '..//div[starts-with(@id, "DOWNLOAD_AND_TRANSFER_DIALOG")]'
short_wait = 0.25
long_wait = 5


def main():
    print("Enter url to download from, should look something like: " + example_url + "\n...")
    url = input()
    init_page = input("Enter page to start from (default 1): ")
    init_page = int(init_page) if init_page else 1

    browser = launch(url)
    download_next_page(url, browser, init_page)


def launch(url):
    browser = Firefox(options=Options())
    browser.get(url)
    input("Press enter once logged in")
    return browser


def download_next_page(url, browser, page_number):
    page_url = f"{url}?pageNumber={page_number}"
    browser.get(page_url)
    time.sleep(long_wait)

    if browser.current_url != page_url:
        print("No more pages")
        quit()
        
    print(f"Downloading page {page_number}")
    download_page(browser)
    download_next_page(url, browser, page_number+1)


def download_page(browser):
    drop_downs = browser.find_elements(By.ID, "dd_title")

    for k, drop_down in enumerate(drop_downs):
        try:
            download_entry(browser, k, drop_down)
        except Exception as e:
            print(f"Could not locate actions for item {k+1}")
            print(e)
        
        ActionChains(browser).click().perform()  # Closes any remaining open dialogue
        time.sleep(short_wait)

    print("Finished downloading page\n")


def download_entry(browser, k, drop_down):
    drop_down.click()
    time.sleep(short_wait)

    try:
        popup = drop_down.find_element(By.XPATH, popup_key)
        download_from_popup(browser, k, popup)

    except Exception as e:
        print(f"Could not locate download action for item {k+1}")
        print(e)


def download_from_popup(browser, k, popup):
    try:
        popup_id = popup.get_attribute("id")[-10:]

        popup.find_element(By.XPATH, "../..").click()
        time.sleep(short_wait)
        popup.find_element(By.ID, f"download_and_transfer_list_{popup_id}_0").click()
        time.sleep(short_wait)
        popup.find_element(By.XPATH, '..//div[contains(@id, "CONFIRM")]').click()
        time.sleep(short_wait)
        browser.find_element(By.ID, "notification-close").click()
        time.sleep(short_wait)
        print(f"Item {k+1} downloaded")
    except Exception as e:
        print(f"Could not download item {k+1}")
        print(e)


if __name__ == "__main__":
    main()
