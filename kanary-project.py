# sync api but can be used in async mode
from playwright.sync_api import sync_playwright, TimeoutError
from bs4 import BeautifulSoup


def extract_img(soup):
    imgs = []
    img_elements = soup.find_all(
        'img', {'class': 'userThumb img-thumbnail lazy'})
    if img_elements is not None:
        for img_element in img_elements:
            imgs.append(img_element['data-src'])
    return imgs


def extract_name(soup):
    names = []
    name_divs = soup.find_all(
        'div', {'class': 'td col col-md-2 name mobile-mt-10'})
    for name_div in name_divs:
        name = name_div.find('strong').text.strip()
        names.append(name)
    return names


def extract_age(soup):
    ages = []
    age_divs = soup.find_all(
        'div', {'class': 'td col col-md-1 age'})
    for age_div in age_divs:
        age = age_div.find('strong').text.strip()
        ages.append(age)
    return ages


def extract_location(soup):
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

    return li_texts


def extract_related_people(soup):
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

    return related_ppl_li_texts


def extract_phone_number(soup):
    phone_numbers = []
    phone_number_divs = soup.find_all(
        'div', {'class': 'td col col-md-2 possible-relatives'})
    if phone_number_divs is not None:
        for phone_number_div in phone_number_divs:
            phone_number = phone_number_div.find('p').text.strip()
            if phone_number is not None:
                phone_numbers.append(phone_number)
    return phone_numbers


def extract_condifential_report_id(soup):
    confidental_report_ids = []
    confidental_report_id_divs = soup.find_all(
        'div', {'class': 'td col col-md-2'})
    for confidental_report_id_div in confidental_report_id_divs:
        confidental_report_id = confidental_report_id_div.find(
            'strong').text.strip()
        confidental_report_ids.append(confidental_report_id)
    return confidental_report_ids


def create_person_dict(imgs, names, ages, locations, related_peoples, phone_numbers, condifential_report_ids):
    person_profiles = []
    print('names len:', len(names))
    if names is not None:
        for i in range(len(names)):
            person = {'img': imgs[i], 'name': names[i], 'age': ages[i], 'location': locations[i],
                      'related people': related_peoples[i], 'phone number': phone_numbers[i], 'condifential report id': condifential_report_ids[i]}
            print('person: ', person)
            person_profiles.append(person)
    return person_profiles


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

            more_button = page.wait_for_selector(
                '//div[@class="row"]//a[contains(text(), "More")]')

            all_profiles = []
            while more_button:
                try:
                    # Extract image src
                    imgs = extract_img(soup)

                    # Extract name
                    names = extract_name(soup)

                    # Extract age
                    ages = extract_age(soup)

                    # Extract location
                    locations = extract_location(soup)

                    # Extract Related People
                    related_peoples = extract_related_people(soup)

                    # extract phone numbers
                    phone_numbers = extract_phone_number(soup)

                    # extract Confidential Report ID
                    condifential_report_ids = extract_condifential_report_id(
                        soup)

                    people_profiles = create_person_dict(
                        imgs, names, ages, locations, related_peoples, phone_numbers, condifential_report_ids)

                    all_profiles += people_profiles
                    more_button.click()

                    # wait for the navigation to complete
                    page.wait_for_load_state()

                    # Get the new more button on the next page
                    more_button = page.wait_for_selector(
                        '//div[@class="row"]//a[contains(text(), "More")]')
                except TimeoutError:
                    print(
                        "Timeout: More button not found within the specified timeout period.")
                    # Get last page
                    # Extract image src
                    imgs = extract_img(soup)

                    # Extract name
                    names = extract_name(soup)

                    # Extract age
                    ages = extract_age(soup)

                    # Extract location
                    locations = extract_location(soup)

                    # Extract Related People
                    related_peoples = extract_related_people(soup)

                    # extract phone numbers
                    phone_numbers = extract_phone_number(soup)

                    # extract Confidential Report ID
                    condifential_report_ids = extract_condifential_report_id(
                        soup)

                    people_profiles = create_person_dict(
                        imgs, names, ages, locations, related_peoples, phone_numbers, condifential_report_ids)

                    all_profiles += people_profiles
                    break

            print(len(all_profiles))
        except:
            print("An error has occurred")
            raise Exception("An error has occurred")


if __name__ == '__main__':
    main()
