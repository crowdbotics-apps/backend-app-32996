APP_CHOICES = [
    ('Web', 'Web'),
    ('Mobile', 'Mobile')
]

FRAMEWORK_CHOICES = [
    ('Django', 'Django'),
    ('React Native', 'React Native')
]


PRICE_CHOICES = [
    ('$0', 'Free ($0)'),
    ('$10', 'Standard ($10)'),
    ('$25', 'Pro ($25)'),
]


APP_CHOICES_LIST = [i[0] for i in APP_CHOICES]
FRAMEWORK_CHOICES_LIST = [i[0] for i in FRAMEWORK_CHOICES]
PRICE_CHOICES_LIST = [i[0] for i in PRICE_CHOICES]
