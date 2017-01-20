wget --output-document=- http://u-go.net/gamerecords/ | grep Download | grep zip | sed 's/.*"\(.*\)".*/\1/' > urls.txt

while read url ; do
    echo "fetching $url"
    wget "$url"
done < urls.txt

echo "Done fetching archive files. Extracting..."


echo "Done!"