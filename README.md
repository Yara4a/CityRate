# CityRate



Authentication System:
Custom User Registration: Developed a CustomUserCreationForm that mandates email input and includes back-end validation to prevent duplicate email registrations.

Session Management: Implemented functional login, signup, and logout views using Django’s authentication framework.

Secure Redirection: Integrated next parameter logic to ensure users are returned to their intended page after authenticating.

Access Control: Applied @login_required decorators to protect sensitive routes like post creation, editing, and deletion.

Automated Testing: Created a suite of unit tests in tests.py to verify email requirements, duplicate prevention, and redirect accuracy.