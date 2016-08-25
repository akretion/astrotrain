#!bin/python
import os
import json

print "resetting template to last git revision for idempotence..."
cmd = 'rm -rf app; rm -rf public/stylesheets; rm public/javascripts; rm -rf  rm -rf data'
os.system(cmd)
cmd = 'git reset --hard HEAD'
print cmd
os.system(cmd)

TODO = [
'mkdir -p app/views',
'git mv snippets app/views/',
'git mv templates app/views/pages',
'git mv layout/theme.liquid app/views/pages',
# TODO move assets in javascript, stylesheet and images",
'mkdir -p public/stylesheets',
'mkdir public/javascripts',
'mkdir public/fonts',
'git mv assets/gift-card.scss.liquid public/stylesheets/gift-card.scss',
'git mv assets/timber.scss.liquid public/stylesheets/timber.scss',
'git mv assets/timber.js.liquid public/javascripts/timber.js',
'git mv assets/ajax-cart.js.liquid public/javascripts/ajax-cart.js',
'git mv assets/*.js* public/javascripts',
'git mv assets/icons* public/fonts',
'git mv app/views/snippets/oldIE-js.liquid app/views/snippets/oldie-js.liquid',
'rmdir layout',
'git rm -rf spec',
'git rm config-sample.yml bower.json circle.yml README.md repodb.yml',
'mkdir app/content_types',
'mkdir data',
'cp ../astrotrain/file/config/* config/',
'cp ../astrotrain/file/project/* .',
]
#

for todo in TODO:
    os.system(todo)

REPLACE = [
    ('| t:', '| translate:'),
    ('| t ', '| translate '),
    ('| script_tag', '| javascript_tag'),
    ('oldIE-js', 'oldie-js'),
    ('| asset_url |', '|'),
    ("{{ settings.logo_max_width | default: '450' | remove: 'px' }}", "450"),

    ('{% if settings.ajax_cart_method == "drawer" %}', ''),
    ('{% endif %} \/\/ settings.ajax_cart_method', ''),
    ('scss.css', 'css'),

# The following replace seem not working
    ('{{ "icons.eot" | asset_url }}', '\/fonts\/icons.eot'),
    ('{{ "icons.woff" | asset_url }}', '\/fonts\/icons.woff'),
    ('{{ "icons.ttf" | asset_url }}', '\/fonts\/icons.ttf'),
    ('{{ "icons.svg" | asset_url }}', '\/fonts\/icons.svg'),


# HACK
    ("{% form 'customer' %}", "{% comment %}{% form 'customer' %}"),
    ("{% endform %}", "{% endform %} {% endcomment %}"),
    ]

f = open('config/settings_data.json')
setting = json.loads(f.read())

for key, value in setting['presets']['Default'].items():
    REPLACE.append(('{{ settings.%s }}' % key, '%s' % value))
    if value == "":
        value = "''"
    elif value == False:
        value = "false"
    elif value == True:
        value = "true"
    elif value == None:
        value = "nil"
    REPLACE.append((' settings.%s ' % key, ' %s ' % str(value))

for old, new in REPLACE:
    cmd = 'find ./ -path ./.git -prune -o -type f -readable -writable -exec sed -i "s/%s/%s/g" {} \;' % (old, new)
    print cmd
    os.system(cmd)


print "Inject theme in view"
os.system('mv app/views/pages/theme.liquid app/views/theme.liquid')
os.system("""cd app/views/pages; find ./ -type f ! -name 'theme.liquid' -exec sed -i "1s/^/{% extends theme %}\\n{% block 'content' %}\\n/" {} \;""")
os.system('cd app/views/pages/; echo "{% endblock %}" | tee -a *.liquid')
os.system('mv app/views/theme.liquid app/views/pages/theme.liquid')
os.system('cd app/views/pages/customers; echo "{% endblock %}" | tee -a *.liquid')
