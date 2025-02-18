import time

from selenium.webdriver import Firefox
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

example_url = "https://www.amazon.co.uk/hz/mycd/digital-console/contentlist/booksAll/dateDsc/"
wait_time = 5  # Time in seconds to give browser second chance at loading a page 


def main():
    print("Enter url to download from (will automatically do future pages)\n\
Should look something like: " + example_url)
    url = input()

    browser = launch(url)
    download_next_page(url, browser, 1)


def launch(url):
    opts = Options()
    browser = Firefox(options=opts)
    browser.get(url)
    input("Press enter once logged in")
    return browser


def download_next_page(url, browser, page_number):
    page_url = f"{url}?pageNumber={page_number}"
    browser.get(page_url)
    time.sleep(wait_time)

    if browser.current_url != page_url:
        print("No more pages")
        quit()
        
    print(f"Downloading page {page_number}")
    download_page(browser)
    download_next_page(url, browser, page_number+1)


def download_page(browser):
    drop_downs = browser.find_elements(By.ID, "dd_title")

    for k, drop_down in enumerate(drop_downs):
        drop_down.click()
        try:
            popup_link = drop_down.find_element(
                        By.XPATH, '..//div[starts-with(@id, "DOWNLOAD_AND_TRANSFER_ACTION")]')
        except Exception:
            print("No download link found for entry")
            close_drop_down(browser, drop_down)
            continue

        download_from_popup_link(browser, popup_link)

    print("All books on page downloaded\n")


def download_from_popup_link(browser, popup_link):
    popup_id = popup_link.get_attribute("id")[-10:]
    popup_link.click()

    click_delayed(browser.find_element, By.ID, f"download_and_transfer_list_{popup_id}_0")
    click_delayed(browser.find_element, By.ID, f"DOWNLOAD_AND_TRANSFER_ACTION_{popup_id}_CONFIRM")
    print(f"{popup_id} downloaded")
    click_delayed(browser.find_element, By.ID, "notification-close")


def close_drop_down(browser, element):
    action = ActionChains(browser)
    action.click()
    action.perform()


def click_delayed(func, *args):
    try:
        func(*args).click()
    except Exception:
        print("\twaiting...")
        time.sleep(wait_time)
        func(*args).click()


if __name__ == "__main__":
    main()
