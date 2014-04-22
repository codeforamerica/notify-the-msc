from selenium import webdriver
import unittest

import os

remote_browser = False
if os.environ.get('NOTIFY_TEST_REMOTE_BROWSER') == "YES":
    remote_browser = True

SAUCE_USERNAME = os.environ.get('SAUCE_USERNAME')
SAUCE_ACCESS_KEY = os.environ.get('SAUCE_ACCESS_KEY')

using_travis = False
hub_url = "%s:%s@localhost:4445" % (SAUCE_USERNAME, SAUCE_ACCESS_KEY)

if 'TRAVIS_JOB_NUMBER' in os.environ:
    using_travis = True
    print "USING TRAVIS", hub_url


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        if remote_browser:
            caps = webdriver.DesiredCapabilities.INTERNETEXPLORER
            caps['platform'] = "Windows XP"
            caps['version'] = "7"
            if using_travis:
                caps['tunnel-identifier'] = os.environ['TRAVIS_JOB_NUMBER']
                print caps
            self.browser = webdriver.Remote(
                command_executor='http://%s/wd/hub' % hub_url,
                desired_capabilities=caps)
        else:
            self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

        # Paramedic opens the app.
        self.browser.get('http://localhost:5000')

    def tearDown(self):
        self.browser.quit()

    def test_can_load_page_and_see_title(self):
        # Paramedic sees that the page title mentions 'Notify the MSC'.
        self.assertIn('Notify the MSC', self.browser.title)

    def test_can_load_page_and_submit_valid_input(self):
        # @todo: Refactor this test.

        # Paramedic sees address field.
        pickup_address_field = self.browser.find_element_by_name('pickup-address')
        self.assertTrue(pickup_address_field.is_displayed())

        # Paramedic sees that address field is labeled 'Pickup address.'
        pickup_address_label = self.browser.find_element_by_id('pickup-address-label')
        self.assertIn('Pickup address', pickup_address_label.text)

        # Paramedic sees hospital field
        hospital_field = self.browser.find_element_by_id('hospital-field')
        self.assertTrue(hospital_field.is_displayed())

        # Paramedic sees "interested?" field
        interested_field = self.browser.find_element_by_id('interested-field')
        self.assertTrue(interested_field.is_displayed())

        # Paramedic sees a submit button that says 'Send to MSC'.
        submit_button = self.browser.find_element_by_id('submit')
        self.assertTrue(submit_button.is_displayed())
        self.assertTrue(submit_button.get_attribute('type') == "submit")
        self.assertIn('Send to MSC', submit_button.text)

        # Paramedic sees a language field -- covered in a test below.

        # Activate a sample language.
        fourth_el_xpath = '//fieldset[@id="language-field"]/div[4]'
        fourth_field_div = self.browser.find_element_by_xpath(fourth_el_xpath)
        fourth_field_div.click()

        # If text has been entered for pickup address, paramedic can submit this field.
        error_box = self.browser.find_element_by_id('error-window')
        success_message = self.browser.find_element_by_id('success-message')

        first_hospital_xpath = '//fieldset[@id="hospital-field"]/div[1]'
        first_hospital_el = self.browser.find_element_by_xpath(first_hospital_xpath)

        first_interested_xpath = '//fieldset[@id="interested-field"]/div[1]'
        first_interested_el = self.browser.find_element_by_xpath(first_interested_xpath)

        first_superutilizer_xpath = '//fieldset[@id="superutilizer-field"]/div[1]'
        first_superutilizer_el = self.browser.find_element_by_xpath(first_superutilizer_xpath)

        pickup_address_field.click()
        pickup_address_field.send_keys('456 elm ave')

        first_hospital_el.click()
        first_interested_el.click()
        first_superutilizer_el.click()

        submit_button.click()
        self.browser.implicitly_wait(3)

        self.assertTrue(success_message.is_displayed())
        self.assertTrue(not error_box.is_displayed())
        self.assertIn('Information successfully submitted', success_message.text)

    def test_hospital_field_input_works(self):
        # Paramedic sees hospital field
        hospital_field = self.browser.find_element_by_id('hospital-field')
        self.assertTrue(hospital_field.is_displayed())

        # Hospital field has an appropriate label
        hospital_label = self.browser.find_element_by_xpath('//fieldset[@id="hospital-field"]/legend')
        self.assertIn(hospital_label.text, "Hospital")

        # Check that there's a button for Memorial
        memorial_button = self.browser.find_element_by_id('hospital-memorial')
        self.assertIn(memorial_button.text, "Memorial")

        # Check that there's a button for St. Mary's
        st_marys_button = self.browser.find_element_by_id('hospital-st-marys')
        self.assertIn(st_marys_button.text, "St. Mary's")

        # Check that there's a button for Community
        community_button = self.browser.find_element_by_id('hospital-community')
        self.assertIn(community_button.text, "Community")

        # Check that there's a button for College (Pacific)
        college_button = self.browser.find_element_by_id('hospital-college')
        self.assertIn(college_button.text, "College (Pacific)")

        # Check that there's a button for Lakewood
        lakewood_button = self.browser.find_element_by_id('hospital-lakewood')
        self.assertIn(lakewood_button.text, "Lakewood")

        # Check that there's a button for Other
        other_button = self.browser.find_element_by_id('hospital-other')
        self.assertIn(other_button.text, "Other")

        # Check that no element is active on load
        active_elements = hospital_field.find_elements_by_class_name('field-active')
        self.assertEquals(0, len(active_elements))

        # Check that clicking a different element makes it active
        fourth_el_xpath = '//fieldset[@id="hospital-field"]/div[4]'
        fourth_field_div = self.browser.find_element_by_xpath(fourth_el_xpath)
        fourth_field_div.click()

        self.assertIn("field-active", fourth_field_div.get_attribute('class'))

    def test_interested_field_input_works(self):
        # Paramedic sees interested field
        interested_field = self.browser.find_element_by_id('interested-field')
        self.assertTrue(interested_field.is_displayed())

        # Interested field has an appropriate label
        interested_label = self.browser.find_element_by_xpath('//fieldset[@id="interested-field"]/legend')
        self.assertIn(interested_label.text, "Is this person interested in talking to a caseworker?")

        # Check that there's a button for Yes
        yes_button = self.browser.find_element_by_id('interested-yes')
        self.assertIn(yes_button.text, "Yes")

        # Check that there's a button for No
        no_button = self.browser.find_element_by_id('interested-no')
        self.assertIn(no_button.text, "No")

        # Check that there's a button for Unsure
        unsure_button = self.browser.find_element_by_id('interested-unsure')
        self.assertIn(unsure_button.text, "Unsure")

        # Check that no element is active on load
        active_elements = interested_field.find_elements_by_class_name('field-active')
        self.assertEquals(0, len(active_elements))

        # Check that clicking a different element makes it active
        second_el_xpath = '//fieldset[@id="interested-field"]/div[2]'
        second_field_div = self.browser.find_element_by_xpath(second_el_xpath)
        second_field_div.click()

        self.assertIn("field-active", second_field_div.get_attribute('class'))

    def test_superutilizer_field_input_works(self):
        # Paramedic sees superutilizer field
        superutilizer_field = self.browser.find_element_by_id('superutilizer-field')
        self.assertTrue(superutilizer_field.is_displayed())

        # Interested field has an appropriate label
        superutilizer_label = self.browser.find_element_by_xpath('//fieldset[@id="superutilizer-field"]/legend')
        self.assertIn(superutilizer_label.text, "Is this person a frequent EMS utilizer?")

        # Check that there's a button for Yes
        yes_button = self.browser.find_element_by_id('superutilizer-yes')
        self.assertIn(yes_button.text, "Yes")

        # Check that no element is active on load
        active_elements = superutilizer_field.find_elements_by_class_name('field-active')
        self.assertEquals(0, len(active_elements))

        # Check that clicking a different element makes it active
        second_el_xpath = '//fieldset[@id="superutilizer-field"]/div[2]'
        second_field_div = self.browser.find_element_by_xpath(second_el_xpath)
        second_field_div.click()

        self.assertIn("field-active", second_field_div.get_attribute('class'))

    def test_can_load_page_and_error_on_no_address(self):
        # If address hasn't been entered, paramedic can't submit this field.
        pickup_address_field = self.browser.find_element_by_name('pickup-address')
        pickup_address_field.clear()
        submit_button = self.browser.find_element_by_id('submit')
        submit_button.click()

        error_box = self.browser.find_element_by_id('error-window')
        success_message = self.browser.find_element_by_id('success-message')

        self.assertTrue(error_box.is_displayed())
        self.assertTrue(not success_message.is_displayed())
        self.assertIn("Please enter an address", error_box.text)

    def test_can_see_language_field(self):  #68918808
        # Paramedic sees language field
        language_field = self.browser.find_element_by_id('language-field')
        self.assertTrue(language_field.is_displayed())

        # Language field has an appropriate label
        language_label = self.browser.find_element_by_xpath('//fieldset[@id="language-field"]/legend')
        self.assertIn(language_label.text, "Language")

        # Paramedic sees the option 'English'.
        english_button = self.browser.find_element_by_id('language-english')
        self.assertIn(english_button.text, "English")

        # Paramedic sees the option 'Spanish'.
        spanish_button = self.browser.find_element_by_id('language-spanish')
        self.assertIn(spanish_button.text, "Spanish")

        # Paramedic sees the option 'Khmer'.
        khmer_button = self.browser.find_element_by_id('language-khmer')
        self.assertIn(khmer_button.text, "Khmer")

        # Paramedic sees the option 'Tagalog'.
        tagalog_button = self.browser.find_element_by_id('language-tagalog')
        self.assertIn(tagalog_button.text, "Tagalog")

        # Paramedic sees the option 'Other'.
        other_button = self.browser.find_element_by_id('language-other')
        self.assertIn(other_button.text, "Other")

        # Check that no element is active on load
        active_elements = language_field.find_elements_by_class_name('field-active')
        self.assertEquals(0, len(active_elements))

        # Check that clicking a different element makes it active
        fourth_el_xpath = '//fieldset[@id="language-field"]/div[4]'
        fourth_field_div = self.browser.find_element_by_xpath(fourth_el_xpath)
        fourth_field_div.click()

        self.assertIn("field-active", fourth_field_div.get_attribute('class'))

    def test_can_submit_language_field(self):  #68918808
        # If an option has been selected, paramedic can submit this field.
        # @TODO: DRY. Maybe combine all of these into one function?

        language_field = self.browser.find_element_by_id('language-field')

        # Check that no element is active on load
        active_elements = language_field.find_elements_by_class_name('field-active')
        self.assertEquals(0, len(active_elements))

        # Check that clicking a different element makes it active
        fourth_el_xpath = '//fieldset[@id="language-field"]/div[4]'
        fourth_field_div = self.browser.find_element_by_xpath(fourth_el_xpath)
        fourth_field_div.click()

        self.assertIn('field-active', fourth_field_div.get_attribute('class'))

    def test_can_load_page_and_error_on_no_language(self):  #68918808
        # @todo: Refactor to use deselectByIndex or deselectByValue instead of filling out everything else?
        # @todo: DRY.
        # If no language has been selected, paramedic can't submit this field.

        pickup_address_field = self.browser.find_element_by_name('pickup-address')

        pickup_address_field.click()
        pickup_address_field.send_keys('456 elm ave')

        # Select a hospital.
        fourth_el_xpath = '//fieldset[@id="hospital-field"]/div[4]'
        fourth_field_div = self.browser.find_element_by_xpath(fourth_el_xpath)
        fourth_field_div.click()

        submit_button = self.browser.find_element_by_id('submit')
        submit_button.click()
        self.browser.implicitly_wait(3)

        error_box = self.browser.find_element_by_id('error-window')
        success_message = self.browser.find_element_by_id('success-message')

        self.assertTrue(error_box.is_displayed())
        self.assertTrue(not success_message.is_displayed())

        self.assertIn("Please select a language", error_box.text)

    def test_can_load_page_and_error_on_no_hospital(self):
        pickup_address_field = self.browser.find_element_by_name('pickup-address')

        pickup_address_field.click()
        pickup_address_field.send_keys('456 elm ave')

        # Select a language.
        fourth_el_xpath = '//fieldset[@id="language-field"]/div[4]'
        fourth_field_div = self.browser.find_element_by_xpath(fourth_el_xpath)
        fourth_field_div.click()

        submit_button = self.browser.find_element_by_id('submit')
        submit_button.click()

        error_box = self.browser.find_element_by_id('error-window')
        success_message = self.browser.find_element_by_id('success-message')

        self.assertTrue(error_box.is_displayed())
        self.assertTrue(not success_message.is_displayed())

        self.assertIn("Please select a hospital", error_box.text)

    def test_can_load_page_and_error_on_no_interested(self):
        pickup_address_field = self.browser.find_element_by_name('pickup-address')

        pickup_address_field.click()
        pickup_address_field.send_keys('456 elm ave')

        # Select a language.
        fourth_el_xpath = '//fieldset[@id="language-field"]/div[4]'
        fourth_field_div = self.browser.find_element_by_xpath(fourth_el_xpath)
        fourth_field_div.click()

        first_hospital_xpath = '//fieldset[@id="hospital-field"]/div[1]'
        first_hospital_el = self.browser.find_element_by_xpath(first_hospital_xpath)
        first_hospital_el.click()

        submit_button = self.browser.find_element_by_id('submit')
        submit_button.click()

        error_box = self.browser.find_element_by_id('error-window')
        success_message = self.browser.find_element_by_id('success-message')

        self.assertTrue(error_box.is_displayed())
        self.assertTrue(not success_message.is_displayed())
        self.assertIn("Please indicate whether the patient is interested in speaking with a caseworker.", error_box.text)

    def test_can_load_page_and_error_on_no_superutilizer(self):
        pickup_address_field = self.browser.find_element_by_name('pickup-address')

        pickup_address_field.click()
        pickup_address_field.send_keys('456 elm ave')

        first_hospital_xpath = '//fieldset[@id="hospital-field"]/div[1]'
        first_hospital_el = self.browser.find_element_by_xpath(first_hospital_xpath)
        first_hospital_el.click()

        first_interested_xpath = '//fieldset[@id="interested-field"]/div[1]'
        first_interested_el = self.browser.find_element_by_xpath(first_interested_xpath)
        first_interested_el.click()

        submit_button = self.browser.find_element_by_id('submit')
        submit_button.click()

        error_box = self.browser.find_element_by_id('error-window')
        success_message = self.browser.find_element_by_id('success-message')

        self.assertTrue(error_box.is_displayed())
        self.assertTrue(not success_message.is_displayed())
        self.assertIn("Please choose if the patient is a frequent EMS utilizer.", error_box.text)
        
if __name__ == '__main__':
    unittest.main()
