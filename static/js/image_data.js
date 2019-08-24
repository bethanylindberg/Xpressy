//parsing data 
var tDataran = JSON.parse(image_data_var);
// console.log(tDataran.length);
// shuffles image selection for carousel
var tData = shuffle(tDataran);
//console.log('Random Data is',tData)

var $imageContent = document.querySelector("#rondellCarousel");

//selecting 20 random images for carousel
for (var i = 0; i < 30; i++) {
  //creating a and div tags 
  var aTag = document.createElement('a');
  var divTag = document.createElement('div');
  //Getting Image ID for an image
  var imageVal = '../static/Stock_Images/Gallery/' + tData[i].Image_ID;
  //populates a tag with required values
  aTag.setAttribute('href', imageVal)
  aTag.setAttribute('target', "_blank")
  aTag.setAttribute('rel', "rondell_1")
  aTag.setAttribute('title', "")
  aTag.setAttribute('id', tData[i].Image_ID)
  //creating and populating img tag
  var imgTag = document.createElement('img');
  imgTag.setAttribute('src', imageVal)

  //creates and populates h5 tags
  var h5Tag = document.createElement('h5');
  h5Tag.innerHTML = tData[i].label
  //appending imag and h5 tags to atag 
  aTag.appendChild(imgTag);
  aTag.appendChild(h5Tag);

  $imageContent.appendChild(aTag);
}

//function to shuffle image pick
function shuffle(imagelist) {
  var ctr = imagelist.length, temp, index;

  // While there are elements in the array
  while (ctr > 0) {
    // Pick a random index
    index = Math.floor(Math.random() * ctr);
    // Decrease ctr by 1
    ctr--;
    // And swap the last element with it
    temp = imagelist[ctr];
    imagelist[ctr] = imagelist[index];
    imagelist[index] = temp;
  }
  return imagelist;
}

//Refers to image related data table
var tableContent = document.querySelector("#tabledata");
//Create Mutation Observer to detect changes
let observer = new MutationObserver(mutationRecords => {
  //Check if data is changed  or only style is changed
  if (mutationRecords[0].addedNodes.length > 0 || mutationRecords[0].removedNodes.length > 0) {
    // if data is changed then it indicates that new image was added and populate data for single image
    var imageContent = document.getElementById('singleImage')
    if (imageContent !== null) {
    var imgid = imageContent.title;
    //Loops through imagelist
    for (i = 0; i < tDataran.length; i++) {
      if (tDataran[i]["Image_ID"] == imgid) {
        tableContent.innerHTML = ""; 
        trhead = document.createElement("tr");
        thead1 = document.createElement("th");
        thead2 = document.createElement("th");
        text1 = document.createTextNode("Emotion");
        text2 = document.createTextNode("Prediction (%)");
        thead1.appendChild(text1);
        thead2.appendChild(text2);
        trhead.appendChild(thead1);
        trhead.appendChild(thead2);
        tableContent.appendChild(trhead);
        //if i matches with imgid populate table as below
        for (var key in tDataran[i]) {
          //populate data for all keys except "Image_ID" and "Label"
          if (String(key) == "Image_ID" || String(key) == "label") {
          } else {
            row = document.createElement("tr");
            cell1 = document.createElement("td");
            cell2 = document.createElement("td");
            textnode1 = document.createTextNode(key);
            textnode2 = document.createTextNode(tDataran[i][key]);
            cell1.appendChild(textnode1);
            cell2.appendChild(textnode2);
            row.appendChild(cell1);
            row.appendChild(cell2);
            tableContent.appendChild(row);
          }
        }
        break;
      }
    }
  } 
  }
  else {
    // if styale is changed then it indicates caurousel mode is on , populate data for focused image
    var imageContent = document.getElementsByClassName("rondell-item rondell-item-focused");
    //console.log('image content is', imageContent)
    if (imageContent[0] !== undefined) {

      var imgid = imageContent[0].id;
      //Loops through Imagelist
      for (i = 0; i < tDataran.length; i++) {
        if (tDataran[i]["Image_ID"] == imgid) {

          tableContent.innerHTML = "";
          trhead = document.createElement("tr");
          thead1 = document.createElement("th");
          thead2 = document.createElement("th");
          text1 = document.createTextNode("Emotion");
          text2 = document.createTextNode("Prediction (%)");
          thead1.appendChild(text1);
          thead2.appendChild(text2);
          trhead.appendChild(thead1);
          trhead.appendChild(thead2);
          tableContent.appendChild(trhead);

          //if i matches with imgid populate table as below
          for (var key in tDataran[i]) {
            //populate data for all keys except "Image_ID" and "Label"
            if (String(key) == "Image_ID" || String(key) == "label") {
            } else {
              row = document.createElement("tr");
              cell1 = document.createElement("td");
              cell2 = document.createElement("td");
              textnode1 = document.createTextNode(key);
              textnode2 = document.createTextNode(tDataran[i][key]);
              cell1.appendChild(textnode1);
              cell2.appendChild(textnode2);
              row.appendChild(cell1);
              row.appendChild(cell2);
              tableContent.appendChild(row);
            }
          }
          break;
        }
      }
    }
  }
});

observer.observe(rondellCarousel, {
  // observe everything except attributes
  childList: true,
  subtree: true,
  attributes: true,
  attributeFilter: ['style']
});

//Gets image_id  of the selected image
/*
function readURL(input) {
  fileName = document.getElementById('fileInputId').files[0].name

  var $imageContent = document.querySelector("#rondellCarousel");
  //selects the div container inside rondellCarousel
  var $imageContentdiv = document.getElementsByClassName('rondell-container');
  //Clears the current image being displayed
  while ($imageContent.firstChild) {
    $imageContent.removeChild($imageContent.firstChild);
  }
  //Creates a and div tags to populate the container with selected image
  var aTag = document.createElement('a');
  var divTag = document.createElement('div');
  divTag.setAttribute('class', "rondell-container rondell-theme-light rondell-instance-1")
  divTag.setAttribute('style', "width: 680px; height: 300px;")

  //populates data for selected image
  var imageVal = 'Stock_Images/Gallery/' + fileName;
  aTag.setAttribute('href', imageVal)
  aTag.setAttribute('target', "_blank")
  aTag.setAttribute('rel', "rondell_1")
  aTag.setAttribute('title', fileName)
  aTag.setAttribute('class', "rondell-item rondell-item-focused")
  aTag.setAttribute('style', "opacity: 1; width: 300px; height: 188px; left: 190px; top: 66px; z-index: 1001; display: block;")


  var imgTag = document.createElement('img');
  imgTag.setAttribute('src', imageVal)
  imgTag.setAttribute('class', "rondell-item-image rondell-item-resizeable")

  var h5Tag = document.createElement('h5');
  //Creates a unque id(singleImage) specific to new image chosen
  aTag.setAttribute('id', 'singleImage');
  h5Tag.innerHTML = imageVal;
  aTag.appendChild(imgTag);
  aTag.appendChild(h5Tag);
  divTag.appendChild(aTag);
  $imageContent.appendChild(divTag);
}
*/