# sync api but can be used in async mode
from playwright.sync_api import sync_playwright, TimeoutError
from bs4 import BeautifulSoup


def extract_img(soup):
    imgs = []
    try:
        img_elements = soup.find_all(
            'img', {'class': 'userThumb img-thumbnail lazy'})
        for img_element in img_elements:
            imgs.append(img_element['data-src'])
    except Exception as e:
        raise Exception(
            f"Error occurred while extracting image URLs: {str(e)}")
    return imgs


def extract_name(soup):
    names = []
    try:
        name_divs = soup.find_all(
            'div', {'class': 'td col col-md-2 name mobile-mt-10'})
        for name_div in name_divs:
            name = name_div.find('strong').text.strip()
            names.append(name)
    except Exception as e:
        raise Exception(f"Error occurred while extracting names: {str(e)}")
    return names


def extract_age(soup):
    ages = []
    try:
        age_divs = soup.find_all('div', {'class': 'td col col-md-1 age'})
        for age_div in age_divs:
            if age_div.find('strong'):
                age = age_div.find('strong').text.strip()
                ages.append(age)
            else:
                ages.append('N/A')
    except Exception as e:
        raise Exception(f"Error occurred while extracting ages: {str(e)}")
    return ages


def extract_location(soup):
    try:
        location_divs = soup.find_all(
            'div', {'class': 'td col col-md-2 location'})

        ul_list = []
        for div_tag in location_divs:
            if div_tag.find('ul'):
                ul_tag = div_tag.find('ul')
                ul_list.append(ul_tag)
            else:
                ul_list.append('N/A')

        li_texts = []
        for ul_tag in ul_list:
            if ul_tag == ['N/A']:
                li_texts.append(['N/A'])
            else:
                li_tags = ul_tag.find_all('li')
                li_texts.append([li_tag.text.strip()
                                for li_tag in li_tags])
    except Exception as e:
        raise Exception(
            f"Error occurred while extracting locations: {str(e)}")

    return li_texts


def extract_related_people(soup):
    try:
        related_ppl_divs = soup.find_all(
            'div', {'class': 'td col col-md-1 possible-relatives'})

        related_ppl_ul_list = []
        for div_tag in related_ppl_divs:
            if div_tag.find('ul'):
                ul_tag = div_tag.find('ul')
                related_ppl_ul_list.append(ul_tag)
            else:
                related_ppl_ul_list.append(['N/A'])

        related_ppl_li_texts = []
        for ul_tag in related_ppl_ul_list:
            if ul_tag == ['N/A']:
                related_ppl_li_texts.append(['N/A'])
            else:
                li_tags = ul_tag.find_all('li')
                related_ppl_li_texts.append(
                    [li_tag.text.strip() for li_tag in li_tags])

    except Exception as e:
        raise Exception(
            f"Error occurred while extracting related peoples: {str(e)}")

    return related_ppl_li_texts


def extract_phone_number(soup):
    phone_numbers = []
    try:
        phone_number_divs = soup.find_all(
            'div', {'class': 'td col col-md-2 possible-relatives'})
        for phone_number_div in phone_number_divs:
            phone_number = phone_number_div.find('p').text.strip()
            phone_numbers.append(phone_number)
    except Exception as e:
        raise Exception(
            f"Error occurred while extracting phone numbers: {str(e)}")
    return phone_numbers


def extract_confidential_report_id(soup):
    confidental_report_ids = []
    try:
        confidental_report_id_divs = soup.find_all(
            'div', {'class': 'td col col-md-2'})
        for confidental_report_id_div in confidental_report_id_divs:
            confidental_report_id = confidental_report_id_div.find(
                'strong').text.strip()
            confidental_report_ids.append(confidental_report_id)
    except Exception as e:
        raise Exception(
            f"Error occurred while extracting confidential report IDs: {str(e)}")
    return confidental_report_ids


def create_person_dict(imgs, names, ages, locations, related_peoples, phone_numbers, confidential_report_ids):
    person_profiles = []
    try:
        if names is not None:
            for i in range(len(names)):
                person = {
                    'img': imgs[i],
                    'name': names[i],
                    'age': ages[i],
                    'location': locations[i],
                    'related people': related_peoples[i],
                    'phone number': phone_numbers[i],
                    'confidential report id': confidential_report_ids[i]
                }
                person_profiles.append(person)
    except Exception as e:
        raise Exception(
            f"Error occurred while creating person profiles: {str(e)}")
    return person_profiles


def extract_person_profiles(soup):
    imgs = extract_img(soup)
    names = extract_name(soup)
    ages = extract_age(soup)
    locations = extract_location(soup)
    related_peoples = extract_related_people(soup)
    phone_numbers = extract_phone_number(soup)
    confidential_report_ids = extract_confidential_report_id(soup)

    # Create person profiles
    people_profiles = create_person_dict(
        imgs, names, ages, locations, related_peoples, phone_numbers, confidential_report_ids)
    return people_profiles


def fill_first_name(page, first_name):
    try:
        input_field = page.wait_for_selector('input.frm-fld-w1')
        input_field.fill(f'{first_name}')
    except Exception as e:
        raise Exception(f"Error in filling first name: {str(e)}")


def fill_last_name(page, last_name):
    try:
        input_field = page.wait_for_selector('input.frm-fld-w2')
        input_field.fill(f'{last_name}')
    except Exception as e:
        raise Exception(f"Error in filling last name: {str(e)}")


def select_state(page, state=None):
    if state is None:
        return
    try:
        state_select = page.wait_for_selector('select[name="state"]')
        state_select.select_option(state)
    except Exception as e:
        raise Exception(f"Error selecting state: {str(e)}")


def main():
    try:
        # context manager
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False, slow_mo=50)
            page = browser.new_page()
            page.goto('https://golookup.com/')

            try:
                # Fill out the search form
                fill_first_name(page, 'stephen')
                fill_last_name(page, 'curry')
                select_state(page, 'CA')
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

                html = page.inner_html('#results')
                soup = BeautifulSoup(html, 'html.parser')

                more_button = page.wait_for_selector(
                    '//div[@class="row"]//a[contains(text(), "More")]')

                all_profiles = []
                while more_button:
                    try:
                        people_profiles = extract_person_profiles(soup)
                        all_profiles += people_profiles
                        more_button.click()

                        # Get the new more button on the next page
                        more_button = page.wait_for_selector(
                            '//div[@class="row"]//a[contains(text(), "More")]')
                    except TimeoutError:
                        print(
                            "Timeout: More button not found within the specified timeout period.")

                        # Get data from the last page
                        # Create person profiles from the last page
                        people_profiles = extract_person_profiles(soup)
                        all_profiles += people_profiles
                        break

                print(all_profiles)
            except:
                raise Exception("An error has occurred on success page load")
    except Exception as e:
        raise Exception("An error has occurred: " + str(e))


if __name__ == '__main__':
    main()
