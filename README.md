# package_statistics


## To run it:
```
 docker run -it kaderno/package_statistics <architecture>
```

Alternatively, you can invoke the python code directly.

The way this program works is: gets the architecture from command line. Checks that the architecture is one of the allowed ones. After that, it creates a temporary file (that gets deleted automatically) and downloads the file from the repository into it. Once the file it's downloaded, it iterates over each of the lines, trying to match every line with the regular expression. If the line is correct, for each package, we insert it into a dictionary to track the number of files that such package has. If the package is not present, we insert it, if it was, the increase the counter (accessing the dictionary has an average complexity of O(1)). 

Once we reach the end of the file, we reverse sorted the dictionary by value (average complexity of O(n log n)) and we return the first 10 packages from the list.

Last, the list is printed.

Most time was spent dealing with the regexp to match correct lines (since there might be free form text on the file), also dealing with downloading and opening gzipped file in an efficient manner and function patching within the test files.
