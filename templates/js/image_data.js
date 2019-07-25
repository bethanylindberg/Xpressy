//parsing data 
var tDataran = JSON.parse(image_data_var);
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
  var imageVal = 'Stock_Images/Gallery/' + tData[i].Image_ID;
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
//Component MutationObserver observes any changes in attribute values and gets them to mutationRecords
let observer = new MutationObserver(mutationRecords => {
  //console.log(mutationRecords); // console.log(the changes)
  var imageContent = document.getElementsByClassName("rondell-item rondell-item-focused");

  if (imageContent[0] !== undefined) {

    var imgid = imageContent[0].id;

    var data = JSON.parse(image_data_var);
    for (i = 0; i < data.length; i++) {
      if (data[i]["Image_ID"] == imgid) {
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

        for (var key in data[i]) {
          if (String(key) == "Image_ID" || String(key) == "label") {
          } else {
            row = document.createElement("tr");
            cell1 = document.createElement("td");
            cell2 = document.createElement("td");
            textnode1 = document.createTextNode(key);
            textnode2 = document.createTextNode(data[i][key]);
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
});
observer.observe(rondellCarousel, {
  // observe everything except attributes
  childList: true,
  subtree: true,
  attributes: true,
  attributeFilter: ['style']
});
