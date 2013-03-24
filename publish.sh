make html
git checkout master
cp -r output/* .
git add .
git commit -am "build $(date)"
git push origin master
git checkout markup
