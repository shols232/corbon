from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six
class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (six.text_type(user.pk) + six.text_type(timestamp)) +  six.text_type(user.is_active)

    # def check_token(self, user, token):
    #     if (self._num_days(self._today()) - ts) > 1:  # 1 day = 24 hours
    #         return False
account_activation_token = AccountActivationTokenGenerator()