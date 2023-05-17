# sync api but can be used in async mode
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup


def main():
    # context manager
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=50)
        page = browser.new_page()
        page.goto('https://golookup.com/')

        try:
            # Fill out the search form
            fill_first_name(page, 'stephen')
            fill_last_name(page, 'curry')
            select_state(page)
            page.click('button[type=submit]')
        except:
            raise Exception('Failed to fill out form')

        # Close both modals
        location_modal_skip_btn = page.wait_for_selector(
            'button:has-text("Skip")', timeout=50000)
        location_modal_skip_btn.click()

        notification_close_btn = page.wait_for_selector(
            '//*[@id="content"]/div/button', timeout=50000)
        notification_close_btn.click()

        try:
            success_text = page.wait_for_selector(
                '//*[@id="content"]/section/div/section/div[1]/div[1]/h3')

            # No records found page
            if not success_text and page.wait_for_selector('//*[@id="content"]/div[2]/div/div/div/div'):
                print('No results found!!')

            # Get the headline text
            headline = page.inner_text('div.headline h3')

            print('headline: ', headline)

            html = page.inner_html('#results')
            soup = BeautifulSoup(html, 'html.parser')

            # # Extract image src
            img_elements = soup.find_all(
                'img', {'class': 'userThumb img-thumbnail lazy'})
            print(img_elements)
            print('img: ', len(img_elements))

            # Extract name
            names = []
            name_divs = soup.find_all(
                'div', {'class': 'td col col-md-2 name mobile-mt-10'})
            for name_div in name_divs:
                name = name_div.find('strong').text
                names.append(name)
            print("Name:", names)
            print("Name:", len(names))

            # Extract age
            ages = []
            age_divs = soup.find_all(
                'div', {'class': 'td col col-md-1 age'})
            for age_div in age_divs:
                age = age_div.find('strong').text
                ages.append(age)
            print("age:", ages)
            print("age:", len(ages))

            # Extract location
            location_divs = soup.find_all(
                'div', {'class': 'td col col-md-2 location'})

            ul_list = []
            for div_tag in location_divs:
                ul_tag = div_tag.find('ul')
                if ul_tag is not None:
                    ul_list.append(ul_tag)

            li_texts = []
            for ul_tag in ul_list:
                li_tags = ul_tag.find_all('li')
                if li_tags is not None:
                    li_texts.append([li_tag.text.strip()
                                    for li_tag in li_tags])

            print("location: ", li_texts)
            print("location:", len(li_texts))
            """
            [<li style="margin-bottom: 4px;">
                1360 ********** **;  Dumas, AR *163*-****
            </li>, <li style="margin-bottom: 4px;">
                17620 ******* 63;  Rison, AR *166*-****
            </li>, <li style="margin-bottom: 4px;">
                1514 ********** **;  Dumas, AR *163*-****
            </li>, <li style="margin-bottom: 4px;">
                612 ** 66;  Dumas, AR *163*-****
            </li>]
            """

            # Extract Related People
            # related_peoples = []
            # related_ppl1 = soup.find_all(
            #     'div', {'class': 'td col col-md-1 possible-relatives'})
            # related_ppl2 = related_ppl1.find('ul')
            # related_ppl_tags = related_ppl2.find_all('li')
            # for related_ppl_tag in related_ppl_tags:
            #     related_peoples.append(related_ppl_tag.text)
            # print("related_ppl:", related_peoples)

            related_ppl_divs = soup.find_all(
                'div', {'class': 'td col col-md-1 possible-relatives'})

            related_ppl_ul_list = []
            for div_tag in related_ppl_divs:
                ul_tag = div_tag.find('ul')
                if ul_tag is not None:
                    related_ppl_ul_list.append(ul_tag)

            related_ppl_li_texts = []
            for ul_tag in related_ppl_ul_list:
                li_tags = ul_tag.find_all('li')
                if li_tags is not None:
                    related_ppl_li_texts.append([li_tag.text.strip()
                                                 for li_tag in li_tags])

            print("related_ppl_li_texts: ", related_ppl_li_texts)
            print("related_ppl_li_texts:", len(related_ppl_li_texts))
            """
            [<li>
                Stephen E Curry
            </li>, <li>
                Christopher Chase Curry
            </li>, <li>
                Jo Ann Curry
            </li>, <li>
                John E Curry
            </li>]
            """

            # phone_numbers
            # phone_number1 = soup.find_all(
            #     'div', {'class': 'td col col-md-2 possible-relatives'})
            # phone_number3 = phone_number1.find('p').text
            # print("phone_number:", phone_number3)

            phone_numbers = []
            phone_number_divs = soup.find_all(
                'div', {'class': 'td col col-md-2 possible-relatives'})
            if phone_number_divs is not None:
                for phone_number_div in phone_number_divs:
                    print('phone_number_div: ', phone_number_div)
                    phone_number = phone_number_div.find('p').text.strip()
                    if phone_number is not None:
                        phone_numbers.append(phone_number)
            print("phone_numbers:", phone_numbers)
            print("phone_numbers:", len(phone_numbers))

            # Confidential Report ID
            # confidental_report_id1 = soup.find_all(
            #     'p', {'class': 'text-center mt-5 fs-mobile-18'})
            # confidental_report_id3 = confidental_report_id1.find('strong').text
            # print("confidental_report_id:", confidental_report_id3)

            confidental_report_ids = []
            confidental_report_id_divs = soup.find_all(
                'div', {'class': 'td col col-md-2'})
            for confidental_report_id_div in confidental_report_id_divs:
                confidental_report_id = confidental_report_id_div.find(
                    'strong').text.strip()
                confidental_report_ids.append(confidental_report_id)
            print("confidental_report_ids:", confidental_report_ids)
            print("confidental_report_ids:", len(confidental_report_ids))
        except:
            print("An error has occurred")
            raise Exception("An error has occurred")


def fill_first_name(page, first_name):
    if not first_name:
        raise ValueError('First name cannot be empty')
    try:
        page.fill('input.frm-fld-w1', f'{first_name}')
    except:
        raise Exception("Error in first name")


def fill_last_name(page, last_name):
    if not last_name:
        raise ValueError('Last name cannot be empty')
    try:
        page.fill('input.frm-fld-w2', f'{last_name}')
    except:
        raise Exception("Error in last name")


def select_state(page, state=None):
    try:
        if state is None:
            return
        else:
            page.select_option('select[name="state"]', state)
    except:
        raise Exception("Error selecting state")


if __name__ == '__main__':
    main()
