#!bin/python
import os

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
'cp ../Astrotrain/file/config/* config/',
'cp ../Astrotrain/file/project/* .',
]
#

for todo in TODO:
    os.system(todo)

REPLACE = [
    ('| t:', '| translate:'),
    ('| t ', '| translate '),
    ('| script_tag', '| javascript_tag'),
    ]

for old, new in REPLACE:
    cmd = 'find ./ -path ./.git -prune -o -type f -readable -writable -exec sed -i "s/%s/%s/g" {} \;' % (old, new)
    print cmd
    os.system(cmd)


