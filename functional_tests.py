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

        # If text has been entered, paramedic can submit this field.
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
        # @TODO: Decide whether to test for these being radio buttons, etc.
        # @TODO: Figure out how to test the radio buttons' associated text.

        # Paramedic sees that this field exists.
        language_field = self.browser.find_element_by_name('language')
        self.assertTrue(language_field.is_displayed())

        # Paramedic sees that this field is labeled 'Language'.
        language_field_label = self.browser.find_element_by_id('language-label')
        self.assertIn('Language', language_field_label.text)

        # Paramedic sees the option 'English'.
        language_option_english = self.browser.find_element_by_id('language-english')

        # Paramedic sees the option 'Spanish'.
        language_option_spanish = self.browser.find_element_by_id('language-spanish')

        # Paramedic sees the option 'Khmer'.
        language_option_khmer = self.browser.find_element_by_id('language-khmer')

        # Paramedic sees the option 'Other'.
        language_option_other = self.browser.find_element_by_id('language-other')

if __name__ == '__main__':
    unittest.main()
