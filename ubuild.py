def main(build):
    build.packages.install("uranium-plus[vscode]")
    build.packages.install("pelican")
    build.packages.install("pelican-gist")
    build.packages.install("../pelican-export", develop=True)
