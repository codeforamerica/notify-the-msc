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

        # Paramedic sees this field.
        pickup_address_field = self.browser.find_element_by_name('pickup-address')
        self.assertTrue(pickup_address_field.is_displayed())

        # Paramedic sees that the field is labeled 'Pickup address.'
        pickup_address_label = self.browser.find_element_by_id('pickup-address-label')
        self.assertIn('Pickup address', pickup_address_label.text)

        # Paramedic sees a submit button that says 'Send to MSC'.
        submit_button = self.browser.find_element_by_id('submit')
        self.assertTrue(submit_button.is_displayed())
        self.assertTrue(submit_button.get_attribute('type') == "submit")
        self.assertIn('Send to MSC', submit_button.text)

        # Paramedic sees a language field -- covered in a test below.

        # Activate a sample language.
        fourth_el_xpath = '//fieldset[@id="language-field"]/div[3]'
        fourth_field_div = self.browser.find_element_by_xpath(fourth_el_xpath)
        fourth_field_div.click()

        # If text has been entered, paramedic can submit this form.
        error_box = self.browser.find_element_by_id('error-window')
        success_message = self.browser.find_element_by_id('success-message')

        pickup_address_field.click()
        pickup_address_field.send_keys('456 elm ave')
        submit_button.click()
        self.browser.implicitly_wait(3)

        self.assertTrue(success_message.is_displayed())
        self.assertTrue(not error_box.is_displayed())
        self.assertIn('Information successfully submitted', success_message.text)

    def test_can_load_page_and_error_on_no_address(self):
        # If address hasn't been entered, paramedic can't submit this field.
        pickup_address_field = self.browser.find_element_by_name('pickup-address')
        pickup_address_field.clear()
        submit_button = self.browser.find_element_by_id('submit')
        submit_button.click()
        self.browser.implicitly_wait(3)
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
        fourth_el_xpath = '//fieldset[@id="language-field"]/div[3]'
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
        fourth_el_xpath = '//fieldset[@id="language-field"]/div[3]'
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

        # @todo: Add hospital element once you've merged it.

        submit_button = self.browser.find_element_by_id('submit')
        submit_button.click()
        self.browser.implicitly_wait(3)

        error_box = self.browser.find_element_by_id('error-window')
        success_message = self.browser.find_element_by_id('success-message')

        self.assertTrue(error_box.is_displayed())
        self.assertTrue(not success_message.is_displayed())
        self.assertIn("Please select a language", error_box.text)

if __name__ == '__main__':
    unittest.main()
