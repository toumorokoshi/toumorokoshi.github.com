make html
git checkout master
git mv output/* .
git add .
git commit -am "build $(date)"
git push origin master
git checkout markup
