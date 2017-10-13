#!/bin/bash

html-minifier --input-dir templates/ --output-dir dist/templates --remove-attribute-quotes --remove-comments --remove-empty-attributes --remove-optional-tags --remove-redundant-attributes --remove-script-type-attributes --remove-style-link-type-attributes --remove-tag-whitespace --trim-custom-fragments --collapse-boolean-attributes --collapse-inline-tag-whitespace --collapse-whitespace

cp -r static dist/
for filename in dist/static/js/*.js; do
    minify --no-comments --output $filename $filename
done
for filename in dist/static/css/*.css; do
    minify --no-comments --output $filename $filename
done
