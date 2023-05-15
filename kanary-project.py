# sync api but can be used in async mode
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup


def main():
    # context manager
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=50)
        page = browser.new_page()
        page.goto('https://golookup.com/')
        fill_first_name(page, 'kevin')
        fill_last_name(page, 'lee')
        select_state(page, 'AL')
        page.click('button[type=submit]')

        # Close both modals
        location_modal_skip_btn = page.wait_for_selector(
            '//*[@id="content"]/section/div[2]/div/div/div/form/div[3]/button[2]')
        print('here: ', location_modal_skip_btn)
        location_modal_skip_btn.click()
        notification_close_btn = page.wait_for_selector(
            '//*[@id="content"]/div/button')
        notification_close_btn.click()

        try:
            success_text = page.wait_for_selector(
                '//*[@id="content"]/section/div/section/div[1]/div[1]/h3')

            if not success_text:
                print('No results found!!')

            # Get the headline text
            headline = page.inner_text('div.headline h3')

            print('headline: ', headline)
        except:
            print("An error has occurred")
            raise Exception("An error has occurred")


def fill_first_name(page, first_name):
    try:
        page.fill('input.frm-fld-w1', f'{first_name}')
    except:
        raise Exception("Error in first name")


def fill_last_name(page, last_name):
    try:
        page.fill('input.frm-fld-w2', f'{last_name}')
    except:
        raise Exception("Error in last name")


def select_state(page, state):
    try:
        page.select_option('select[name="state"]', state)
    except:
        raise Exception("Error selecting state")


if __name__ == '__main__':
    main()
