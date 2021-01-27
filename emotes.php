<DOCTYPE html>
<html>
<head>
<title>MarisaBot Emotes</title>
<link href="./index.css" rel="stylesheet" typ="test/css" />
<script src="http://www.widdiful.co.uk/files/js/jQuery.js" type="text/javascript"></script>
<script src="http://www.widdiful.co.uk/files/js/jquery.mousewheel-3.0.6.pack.js" type="text/javascript"></script>
<link rel="stylesheet" href="./js/jquery.fancybox.css?v=2.1.5" type="text/css" media="screen" />
<script type="text/javascript" src="./js/jquery.fancybox.pack.js?v=2.1.5"></script>
<link rel="stylesheet" href="./js/helpers/jquery.fancybox-buttons.css?v=1.0.5" type="text/css" media="screen" />
<script type="text/javascript" src="./js/helpers/jquery.fancybox-buttons.js?v=1.0.5"></script>
<script type="text/javascript" src="./js/helpers/jquery.fancybox-media.js?v=1.0.6"></script>
<link rel="stylesheet" href="./js/helpers/jquery.fancybox-thumbs.css?v=1.0.7" type="text/css" media="screen" />
<script type="text/javascript" src="./js/helpers/jquery.fancybox-thumbs.js?v=1.0.7"></script>
<script>
  $(document).ready(function(){
    $('.img-zoom').hover(function() {
        $(this).addClass('transition');
 
    }, function() {
        $(this).removeClass('transition');
    });
  });
</script>
<script type="text/javascript">
	$(document).ready(function() {
		$(".fancybox").fancybox({
			prevEffect	: 'elastic',
			nextEffect	: 'elastic',
			helpers	: {
				thumbs	: {
					width	: 50,
					height	: 50
				}
			}
		});
	});
</script>
<script>
function toggleBG()
{
	if (document.body.style.backgroundColor == 'rgb(54, 57, 62)'){
		document.body.style.backgroundColor = 'rgb(255, 255, 255)';
	}
	else {
		document.body.style.backgroundColor = 'rgb(54, 57, 62)';
	}
}

function toggleHidden(){
	if (document.getElementById("checkbox").checked){
		var elements = document.getElementsByClassName("hidden")

		for (var i = 0; i < elements.length; i++){
			elements[i].style.display = "inline-block";
		}
	}
	else{
		var elements = document.getElementsByClassName("hidden")

		for (var i = 0; i < elements.length; i++){
			elements[i].style.display = "none";
		}
	}
}
</script>
<style>
.collapsible {
  background-color: #777;
  color: white;
  cursor: pointer;
  padding: 18px;
  width: 100%;
  border: none;
  text-align: left;
  outline: none;
  font-size: 15px;
}

.active, .collapsible:hover {
  background-color: #555;
}

.collapsed {
  padding: 0 18px;
  display: none;
  overflow: hidden;
  background-color: #f1f1f1;
}
</style>
</head>
<body>
<button type="button" onclick="toggleBG()">Theme</button>
<input type="checkbox" id = "checkbox" onclick="toggleHidden()">Show All</button>
<div id="content">
	<?php
function createThumbnail($image_name,$new_width,$new_height,$uploadDir,$moveToDir)
{
  $path = $uploadDir . '/' . $image_name;

  $mime = getimagesize($path);

  if($mime['mime']=='image/png') { 
      $src_img = imagecreatefrompng($path);
  }
  if($mime['mime']=='image/jpg' || $mime['mime']=='image/jpeg' || $mime['mime']=='image/pjpeg') {
      $src_img = imagecreatefromjpeg($path);
  }   

  $old_x          =   imageSX($src_img);
  $old_y          =   imageSY($src_img);

  if($old_x > $old_y) 
  {
      $thumb_w    =   $new_width;
      $thumb_h    =   $old_y*($new_height/$old_x);
  }

  if($old_x < $old_y) 
  {
      $thumb_w    =   $old_x*($new_width/$old_y);
      $thumb_h    =   $new_height;
  }

  if($old_x == $old_y) 
  {
      $thumb_w    =   $new_width;
      $thumb_h    =   $new_height;
  }

  $dst_img        =   ImageCreateTrueColor($thumb_w,$thumb_h);

  imagecopyresampled($dst_img,$src_img,0,0,0,0,$thumb_w,$thumb_h,$old_x,$old_y); 


  // New save location
  $new_thumb_loc = $moveToDir . $image_name;

  if($mime['mime']=='image/png') {
      $result = imagepng($dst_img,$new_thumb_loc,8);
  }
  if($mime['mime']=='image/jpg' || $mime['mime']=='image/jpeg' || $mime['mime']=='image/pjpeg') {
      $result = imagejpeg($dst_img,$new_thumb_loc,80);
  }

  imagedestroy($dst_img); 
  imagedestroy($src_img);

  return $result;
}
    
$files = glob("emotes/*.*");
usort($files, 'strnatcasecmp');
$prev = '?';
echo 'total emotes: ' . count($files) . '</br>' . 'randoms: gun, shades, smug, stare, thumbsup (use !randemote)' . '</br></br>';

echo '<form action="emotes.php" method="get">Search: <input type="text" name="search_query" ';
if (isset($_GET["search_query"]) && !isset($_GET["clear_search"])) {
  echo 'value=' . filter_var($_GET["search_query"], FILTER_SANITIZE_STRING);
}
echo '> <input type="submit" name="form_submit" value="Search"> <input type="submit" name="clear_search" value="Clear"><br></form>';

if (isset($_GET["search_query"]) && isset($_GET["form_submit"]) && $_GET["form_submit"] === "Search") {
  $needle = filter_var($_GET["search_query"], FILTER_SANITIZE_STRING);

  $filtered = [];
  if ($needle !== "") {
    $filtered = array_values(array_filter($files, function($image) use ($needle) {
      $fname = str_replace("`Q", "?", pathinfo($image, PATHINFO_FILENAME));
      return strpos($fname, $needle) !== false;
    }));
  }

  echo '<button class="collapsible">' . count($filtered) . ' search results for query "' . $needle . '"</button><div>';
  for ($i = 0; $i < count($filtered); $i++) {
    $image = $filtered[$i];
    $fname = str_replace("`Q", "?", pathinfo($image, PATHINFO_FILENAME));

    if (strpos($fname, $needle) === false) {
      continue;
    }

    $next = strtoupper($image[7]);
      
    $hidden = substr($fname, -1) === "~";
      
    if (is_numeric($next)){
      $next = "0-9";
    }
    if ($next != $prev){
      echo '</br></br><table width="100%"><tr bgcolor="ADDFAD"><th>' . $next . '</th></tr></table></br>';
    }
    if (!$hidden){
      echo '<a class="fancybox" title="!' . $fname . '"rel="group" href="' . $image . '"><img class="img-zoom" src="' . $image .'"></a>';
    }
    else {
      echo '<a class="hidden" style="display:none" class="fancybox" title="!' . $fname . '"rel="group" href="' . $image . '"><img class="img-zoom" src="' . $image .'"></a>';
    }
    $prev = $next;
  }
  echo '</div>';
} else {
  echo '<button class="collapsible">Text list</button><div class="collapsed">';
  for ($i = 0; $i < count($files); $i++) {
    $image = $files[$i];
    $next = strtoupper($image[7]);
    $fname = str_replace("`Q", "?", pathinfo($image, PATHINFO_FILENAME));
      
    $hidden = substr($fname, -1) === "~";
      
    if (is_numeric($next)){
      $next = "0-9";
    }
    if ($next != $prev){
      echo '<br><br><b>' . $next . '</b></br>';
    }
    echo '!' . $fname . ', ';
    $prev = $next;

  }
  echo '</div>';

  for ($i = 0; $i < count($files); $i++) {
    $image = $files[$i];
    $next = strtoupper($image[7]);
    $fname = str_replace("`Q", "?", pathinfo($image, PATHINFO_FILENAME));
      /*$imagesmall = "emotes/resized/" . pathinfo($image, PATHINFO_BASENAME);
      if (pathinfo($image, PATHINFO_EXTENSION) == "jpg" || pathinfo($image, PATHINFO_EXTENSION) == "png"){
          if (!file_exists($imagesmall)){
              createThumbnail(pathinfo($image, PATHINFO_BASENAME), 300, 300, "emotes", "emotes/resized/");
          }
      }
      else{
          $imagesmall = $image;
      }*/
    $hidden = substr($fname, -1) === "~";
      
    if (is_numeric($next)){
      $next = "0-9";
    }
    if ($next != $prev){
      echo '</br></br><table width="100%"><tr bgcolor="ADDFAD"><th>' . $next . '</th></tr></table></br>';
    }
    if (!$hidden){
      echo '<a class="fancybox" title="!' . $fname . '"rel="group" href="' . $image . '"><img class="img-zoom" src="' . $image .'"></a>';
    }
    else {
      echo '<a class="hidden" style="display:none" class="fancybox" title="!' . $fname . '"rel="group" href="' . $image . '"><img class="img-zoom" src="' . $image .'"></a>';
    }
    $prev = $next;

  }
}
?>
</a>
</div>
<script>
var coll = document.getElementsByClassName("collapsible");
var i;

for (i = 0; i < coll.length; i++) {
  coll[i].addEventListener("click", function() {
    this.classList.toggle("active");
    var content = this.nextElementSibling;
    if (content.style.display === "block") {
      content.style.display = "none";
    } else {
      content.style.display = "block";
    }
  });
}
</script>
</body>
</html>
