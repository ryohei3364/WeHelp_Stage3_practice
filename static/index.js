const uploadButton = document.getElementById("upload--button");
const fileInput = document.getElementById("input--file");
const container = document.getElementById("show--content");
const list = document.getElementById("show--list");
const submitButton = document.getElementById("submit--button");
const textInput = document.getElementById("input--text");
const fileResult = document.getElementById("file--result");

let selectedFile = null;
let imageUrl = null;

uploadButton.addEventListener('click', () => {
  fileInput.click();

  fileInput.onchange = async () => {
    selectedFile = fileInput.files[0];
    if (!selectedFile) return;

    submitButton.disabled = true; 
    fileResult.textContent = selectedFile.name;

    const formData = new FormData();
    formData.append('file', selectedFile);
    try {
      const response = await fetch("/api/upload", {
        method: "POST",
        body: formData,
      });
      const result = await response.json();

      if (result.url) {
        imageUrl = result.url; 
        submitButton.disabled = false; 
      }
    } catch (error) {
    }
    fileInput.value = "";
  };
});

submitButton.addEventListener('click', async () => {
  if (textInput.value && imageUrl) {
    const formSubmit = new FormData();
    formSubmit.append('content', textInput.value); 
    formSubmit.append('imageUrl', imageUrl); 
    try{
      const response = await fetch("/api/submit", {
        method: "POST",
        body: formSubmit,
      });
      const result = await response.json();  
      renderPost(result.data, true);
    } catch (error) {
      console.error("Error uploading file:", error);
    }
  }
});


function renderPost(post, toTop = true) {
  const wrapper = document.createElement("div");
  wrapper.className = "wrapper";

  const text = document.createElement("span");
  text.textContent = post.content;

  const img = document.createElement("img");
  img.src = post.image_url;
  img.alt = "上傳圖片";

  const divider = document.createElement("div");
  divider.className = "divider";

  wrapper.appendChild(text);
  wrapper.appendChild(img);
  wrapper.appendChild(divider);

  if (toTop) {
    container.prepend(wrapper); 
  } else {
    container.appendChild(wrapper);
  }
}

window.addEventListener("DOMContentLoaded", async () => {
  try {
    const response = await fetch("/api/posts");
    const result = await response.json();

    const posts = result.data;
    if (posts) {
      posts.forEach(post => renderPost(post, false));
    } else {
      return;
    }
  } catch (error) {
    console.error("載入資料時發生錯誤", error);
  }
});