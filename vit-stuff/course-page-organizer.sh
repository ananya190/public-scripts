#!/bin/sh

# take path as argument
path=$1
unzipdir=$2

# if unzip directory is not specified, echo error and exit
if [ -z "$unzipdir" ]; then
    echo "Error: unzip directory not specified"
    exit 1
fi

# if unzip dir has a trailing slash, remove it
if [ "${unzipdir: -1}" = "/" ]; then
    unzipdir=${unzipdir%?}
fi

# append to pwd if path is not absolute
if [ "${path:0:1}" != "/" ]; then
    path=$(pwd)/$path
fi

echo $path

# if the path is a zip file, unzip it and set path to the unzipped directory
if [ "${path: -4}" = ".zip" ]; then
    filename=$(basename "$path")
    echo "zip file"
    mkdir -p "$(pwd)/$unzipdir"
    echo "$(pwd)/$unzipdir"
    echo $path
    unzip "$path" -d "$(pwd)/$unzipdir"
    path="$(pwd)/$unzipdir/"
    # path="${path%.*}"
fi

# read course code from user
read -p "Enter course code: " coursecode
# make directory under path for Syllabus; path has a slash at the end
mkdir -p "$path""Syllabus_Textbook"
# mkdir -p "$path"Syllabus

mv "$path"$coursecode*.pdf "$path"Syllabus_Textbook/
# if filename has syllabus or textbook, or Syllabus or Textbook, move to Syllabus
mv "$path"*Syllabus*.pdf "$path"Syllabus_Textbook/
mv "$path"*Textbook*.pdf "$path"Syllabus_Textbook/
mv "$path"*syllabus*.pdf "$path"Syllabus_Textbook/
mv "$path"*textbook*.pdf "$path"Syllabus_Textbook/


# ls the Syllabus directory
ls "$path"Syllabus


echo "$path"

# display prompt asking if this is a dry run or the actual run
echo "Is this a dry run or the actual run?"
echo "1) Dry run"
echo "2) Actual run"
read -p "Enter 1 or 2: " dry_run

# display dry run status
if [ $dry_run -eq 1 ]; then
    echo "Dry run"
else
    echo "Actual run"
fi

# set variable count to 0
count=0

# loop through each file in the directory with extension docx, doc, ppt and pdf
# create array with file types appended to path
path_arr=("$path"*.{pptx,docx,doc,ppt,pdf})
# display path_arr with newlines
echo "${path_arr[@]}"

# use the array to loop through each file
for file in "${path_arr[@]}"
do
    # if the file doesn't exist, skip it
    if [ ! -f "$file" ]; then
        continue
    fi
    # increment count
    count=$((count+1))
    echo $file
    # extract filename without extension
    filename=$(basename "$file")
    echo $filename
    extension="${filename##*.}"
    echo $extension
    # filename="${filename%.*}"
    echo $filename
    # set the filename to be the substring after the fifth underscore
    filename=$(echo $filename | cut -d'_' -f7-)
    echo $filename
    # from the filename, extract the substring before the first underscore
    number="${filename%%_*}"
    # if number is I, set it to 1, II to 2, etc.
    if [ "$number" = "I" ]; then
        number=1
    elif [ "$number" = "II" ]; then
        number=2
    elif [ "$number" = "III" ]; then
        number=3
    elif [ "$number" = "IV" ]; then
        number=4
    elif [ "$number" = "V" ]; then
        number=5
    fi
    # extract the date in dd-mm-yyyy format from the filename
    thisdate=$(echo $filename | grep -o -E '[0-9]{2}-[0-9]{2}-[0-9]{4}')
    echo $thisdate
    # convert the date to yyyy-mm-dd format
    thisdate=$(date -jf %d-%m-%Y -- "$thisdate" +%F)
    
    echo $thisdate
    # extract the substring after the second underscore - the title (I_dd-mm-yyyy-title)
    title=$(echo $filename | cut -d'_' -f3-)
    echo $title
    # create the new filename as date-number_title.extension
    newfilename="$thisdate-$number"_"$title"
    echo  $count mv $file "$path"$newfilename
    # if this is a dry run, display the mv command to be executed
    if [ "$dry_run" = "1" ]; then
        echo $count mv $file "$path""$newfilename"
    # if this is the actual run, execute the mv command
    elif [ "$dry_run" = "2" ]; then
        mv "$file" "$path""$newfilename"
    fi
done
