import time
import pytest
from ads_vk_test_base import BaseCase
from ui.pages.ads_vk_landing import LandingPage


class TestSettings(BaseCase):
    authorize = True

    # not really a teardown due to inability to actually delete a newly created profile
    @pytest.fixture(autouse=True)
    def setup_settings(self):
        try:
            self.landing_page.login()
            self.register_page = self.landing_page.create_account_profile_exists()
        except:
            self.landing_page.reopen()
            self.landing_page.login()
            self.register_page = self.landing_page.create_account_new_profile()
        
        self.lk_page = self.register_page.register_advertiser_physical("roflanpotsan@ya.ru", should_redirect=True)
        self.settings_page = self.lk_page.open_general_settings()

        yield

        self.settings_page.delete_lk()
        self.settings_page.wait().until(lambda driver: driver.current_url == self.landing_page.url)

    def test_cancel_changes(self):
        self.settings_page.set_lk_name('Рофлан-лицо')
        self.settings_page.cancel_changes()
        assert self.settings_page.get_lk_name() == ''

    def test_save_changes(self):
        new_name = 'Рофлан-лицо'
        new_tpid = '145047727543'
        self.settings_page.set_lk_name(new_name)
        self.settings_page.set_lk_tax_payer_id(new_tpid)
        self.settings_page.save_changes()
        self.settings_page.reload()

        assert self.settings_page.get_lk_name() == new_name
        assert self.settings_page.get_lk_tax_payer_id() == new_tpid

    def test_add_email(self):
        email = "roflanpotsan@yandex.ru"
        new_name = 'Рофлан-лицо'
        new_tpid = '145047727543'
        self.settings_page.set_lk_name(new_name)
        self.settings_page.set_lk_tax_payer_id(new_tpid)
        self.settings_page.add_email(email)
        self.settings_page.save_changes()
        self.settings_page.reload()
        assert email in self.settings_page.get_email_confirmation_msg()

    def test_request_api_access(self):
        new_name = 'Рофлан-лицо'
        new_tpid = '145047727543'
        self.settings_page.set_lk_name(new_name)
        self.settings_page.set_lk_tax_payer_id(new_tpid)
        self.settings_page.save_changes()
        self.settings_page.reload()
        self.settings_page.request_api_access(phone='+1231231231231')
        assert self.settings_page.get_api_key() != ""

    def test_update_notifications(self):
        self.settings_page.open_notification_settings_tab()
        self.settings_page.toggle_all_notifications()
        self.settings_page.save_changes()
        self.settings_page.reload()
        self.settings_page.open_notification_settings_tab()

        assert len(self.settings_page.get_notifications_list()) == 0

    # def test_add_lk_access(self):
    #     self.settings_page.switch_to_first_accout()
    #     self.lk_page.open_general_settings()
    #     lk_id = self.settings_page.get_lk_id()

    #     self.settings_page.switch_to_current_account()
    #     self.lk_page.open_general_settings()
    #     self.settings_page.open_access_settings_tab()
    #     self.settings_page.create_access(lk_id)
    #     self.settings_page.remove_access()
