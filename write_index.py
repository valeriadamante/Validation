# python script that writes the index.php file
import os
def write_php_file(dir): 
    if not os.path.exists(dir+"index.php"):
        print dir+"index.php non esiste"
        f = open(dir+"index.php", "w")
        f.write("<html> \n<head> \n<title><?php echo getcwd(); ?></title>\n<style type='text/css'>\nbody { \n\t\tfont-family: \"Candara\", sans-serif; \n\t\tfont-size: 9pt; \n\t\tline-height: 10.5pt; \n}\ndiv.pic h3 { \n\t\tfont-size: 11pt; \n\t\tmargin: 0.5em 1em 0.2em 1em; \n} \ndiv.pic p { \n\t\tfont-size: 11pt;\n\t\tmargin: 0.2em 1em 0.1em 1em;\n}\ndiv.pic {\n\t\tdisplay: block;\n\t\tfloat: left; \n\t\tbackground-color: white; \n\t\tborder: 1px solid #ccc; \n\t\tpadding: 2px; \n\t\ttext-align: center; \n\t\tmargin: 2px 10px 10px 2px; \n\t\t-moz-box-shadow: 7px 5px 5px rgb(80,80,80);\t\t\t/* Firefox 3.5 */\n\t\t-webkit-box-shadow: 7px 5px 5px rgb(80,80,80);\t/* Chrome, Safari */\n\t\tbox-shadow: 7px 5px 5px rgb(80,80,80);\t\t\t\t\t/* New browsers */\n}\na { text-decoration: none; color: rgb(80,0,0); }\na:hover { text-decoration: underline; color: rgb(255,80,80); }\ndiv.dirlinks h2 {  margin-bottom: 4pt; margin-left: -24pt; color: rgb(80,0,0);  }\ndiv.dirlinks {  margin: 0 24pt; } \ndiv.dirlinks a {\n\t\tfont-size: 11pt; font-weight: bold;\n\t\tpadding: 0 0.5em; \n}\n</style>\n</head>\n<body> \n<h1><?php echo getcwd(); ?></h1> \n<?php \n$has_subs = false; \nforeach (glob(\"*\") as $filename) { \n\t\tif (is_dir($filename) && !preg_match(\"/^\..*|.*private.*/\", $filename)) { \n\t\t\t\t$has_subs = true; \n\t\t\t\tbreak; \n\t\t} \n} \nif ($has_subs) { \n\t\tprint \"<div class=\\\"dirlinks\\\">\\n\"; \n\t\tprint \"<h2>Directories</h2>\\n\"; \n\t\tprint \"<a href=\\\"../\\\">[parent]</a> \"; \n\t\tforeach (glob(\"*\") as $filename) { \n\t\t\t\tif (is_dir($filename) && ($_SERVER['PHP_AUTH_USER'] == \'gpetrucc\' || !preg_match(\"/^\..*|.*private.*/\", $filename))) { \n\t\t\t\t\t\tprint \" <a href=\\\"$filename\\\">[$filename]</a>\"; \n\t\t\t\t} \n\t\t} \n\t\tprint \"</div>\"; \n} \n\nforeach (array(\"00_README.txt\", \"README.txt\", \"readme.txt\") as $readme) { \n\t\tif (file_exists($readme)) {  \n\t\t\t\tprint \"<pre class='readme'>\\n\"; readfile($readme); print \"</pre>\"; \n\t\t} \n} \n?> \n\n<h2><a name=\"plots\">Plots</a></h2>\n<p><form>Filter: <input type=\"text\" name=\"match\" size=\"30\" value=\"<?php if (isset($_GET['match'])) print htmlspecialchars($_GET['match']);  ?>\" /><input type=\"Submit\" value=\"Go\" /><input type=\"checkbox\"  name=\"regexp\" <?php if ($_GET['regexp']) print \"checked=\\\"checked\\\"\"?> >RegExp</input></form></p>\n<div>\n<?php\n$displayed = array();\nif ($_GET['noplots']) {\n\t\tprint \"Plots will not be displayed.\\n\";\n} else {\n\t\t$other_exts = array('.pdf', '.cxx', '.eps', '.root', '.txt', '.dir');\n\t\t$filenames = glob(\"*.png\"); sort($filenames);\n\t\tforeach ($filenames as $filename) {\n\t\t\t\tif (isset($_GET['match'])) {\n\t\t\t\t\t\t if (isset($_GET['regexp']) && $_GET['regexp']) {\n\t\t\t\t\t\t\t\tif (!preg_match('/.*'.$_GET['match'].'.*/', $filename)) continue;\n\t\t\t\t\t\t } else {\n\t\t\t\t\t\t\t\tif (!fnmatch('*'.$_GET['match'].'*', $filename)) continue;\n\t\t\t\t\t\t } \n\t\t\t\t}\n\t\t\t\tarray_push($displayed, $filename);\n\t\t\t\tprint \"<div class='pic'>\\n\";\n\t\t\t\tprint \"<h3><a href=\\\"$filename\\\">$filename</a></h3>\";\n\t\t\t\tprint \"<a href=\\\"$filename\\\"><img src=\\\"$filename\\\" style=\\\"border: none; width: 300px; \\\"></a>\"; \n\t\t\t\t$others = array();\n\t\t\t\tforeach ($other_exts as $ex) {\n\t\t\t\t\t\t$other_filename = str_replace('.png', $ex, $filename);\n\t\t\t\t\t\tif (file_exists($other_filename)) {\n\t\t\t\t\t\t\t\tarray_push($others, \"<a class=\\\"file\\\" href=\\\"$other_filename\\\">[\" . $ex . \"]</a>\");\n\t\t\t\t\t\t\t\tif ($ex != '.txt') array_push($displayed, $other_filename);\n\t\t\t\t\t\t}\n\t\t\t\t}\n\t\t\t\tif ($others) print \"<p>Also as \".implode(', ',$others).\"</p>\";\n\t\t\t\tprint \"</div>\";\n\t\t}\n}\n?>\n</div>\n<div style=\"display: block; clear:both;\">\n<h2><a name=\"files\">Other files</a></h2>\n<ul>\n<?\nforeach (glob(\"*\") as $filename) {\n\t\tif ($_GET['noplots'] || !in_array($filename, $displayed)) {\n\t\t\t\tif (isset($_GET['match'])) {\n\t\t\t\t\t\t if (isset($_GET['regexp']) && $_GET['regexp']) {\n\t\t\t\t\t\t\t\tif (!preg_match('/.*'.$_GET['match'].'.*/', $filename)) continue;\n\t\t\t\t\t\t } else {\n\t\t\t\t\t\t\t\tif (!fnmatch('*'.$_GET['match'].'*', $filename)) continue;\n\t\t\t\t\t\t }\n\t\t\t\t}\n\t\t\t\tif (is_dir($filename)) {\n\t\t\t\t\t\tprint \"<li>[DIR] <a href=\\\"$filename\\\">$filename</a></li>\";\n\t\t\t\t} else {\n\t\t\t\t\t\tprint \"<li><a href=\\\"$filename\\\">$filename</a></li>\";\n\t\t\t\t}\n\t\t}\n}\n?>\n</ul>\n</div>\n</body>\n</html>\n")
        f.close()