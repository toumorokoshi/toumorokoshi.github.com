# download blog posts from dropbox
curl -X POST https://content.dropboxapi.com/2/files/download_zip \
  --header "Authorization: Bearer $DROPBOX_ACCESS_TOKEN" \
  --header 'Dropbox-API-Arg: {"path":"/docs/blog"}' --output /tmp/blog.zip
unzip -o /tmp/blog.zip
cp -rv blog/* .
rm -r blog