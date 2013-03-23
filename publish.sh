make html
git checkout master
mv output/* .
git add .
git commit -am "build $(date)"
git push origin master
git checkout markup
