document.addEventListener('DOMContentLoaded', function() {
  const navLinks = document.querySelectorAll('.nav a');
  const contents = document.querySelectorAll('.content');
  const fileInput = document.getElementById('fileInput');
  const uploadArea = document.getElementById('uploadArea');
  const filesList = document.getElementById('filesList');
  const startConversion = document.getElementById('startConversion');
  const addFilesButton = document.getElementById('addFiles');
  const clearFilesButton = document.getElementById('clearFiles');

  // 假设后端返回的音频格式数组
  const audioFormats = ['MP3', 'WAV', 'AAC', 'FLAC'];
  const formatOptionsContainer = document.getElementById('formatOptions');
  const startConversionButton = document.getElementById('startConversion');

  // 动态生成音频格式选项
  audioFormats.forEach(format => {
    const radioInput = document.createElement('input');
    radioInput.type = 'radio';
    radioInput.name = 'outputFormat';
    radioInput.id = `format-${format.toLowerCase()}`;
    radioInput.value = format;

    const radioLabel = document.createElement('label');
    radioLabel.className = 'radio-label';
    radioLabel.setAttribute('for', `format-${format.toLowerCase()}`);
    radioLabel.textContent = format;

    formatOptionsContainer.appendChild(radioInput);
    formatOptionsContainer.appendChild(radioLabel);
  });

  // 当用户点击“开始转换”按钮时，检查是否选择了输出格式
  startConversionButton.addEventListener('click', function () {
    const selectedFormat = document.querySelector('input[name="outputFormat"]:checked');
    if (!selectedFormat) {
      alert('请先选择输出格式！');
    } else {
      // 用户已选择输出格式，可以进行转换操作
      console.log('Selected Format:', selectedFormat.value);
      // 这里可以添加实际的转换逻辑
    }
  });


  // 切换内容
  navLinks.forEach(link => {
    link.addEventListener('click', e => {
      e.preventDefault();
      const targetTab = e.target.getAttribute('data-tab');
      contents.forEach(content => {
        content.classList.remove('active');
      });
      document.getElementById(targetTab).classList.add('active');
      navLinks.forEach(navLink => {
        navLink.classList.remove('active');
      });
      e.target.classList.add('active');
    });
  });

  // 文件操作
  addFilesButton.addEventListener('click', () => fileInput.click());
  clearFilesButton.addEventListener('click', () => {
    while (filesList.firstChild) {
      filesList.removeChild(filesList.firstChild);
    }
    checkStartButtonState();
  });

  // uploadArea.addEventListener('click', () => fileInput.click());
  uploadArea.addEventListener('dragover', e => e.preventDefault());
  uploadArea.addEventListener('drop', handleDrop);

  fileInput.addEventListener('change', handleFiles);
  startConversion.addEventListener('click', startConversionProcess);

  function handleFiles(e) {
    for (const file of e.target.files) {
      addFileToList(file);
    }
    checkStartButtonState();
  }

  function handleDrop(e) {
    e.preventDefault();
    for (const file of e.dataTransfer.files) {
      addFileToList(file);
    }
    checkStartButtonState();
  }

  function addFileToList(file) {
    const li = document.createElement('li');
    li.textContent = file.name;
    const removeBtn = document.createElement('button');
    removeBtn.textContent = '删除';
    removeBtn.onclick = () => {
      li.remove();
      checkStartButtonState();
    };
    li.appendChild(removeBtn);
    filesList.appendChild(li);
  }

  function checkStartButtonState() {
    if (filesList.children.length > 0) {
      startConversion.disabled = false;
    } else {
      startConversion.disabled = true;
    }
  }

  function startConversionProcess() {
    if (filesList.children.length > 10) {
      alert('您不能上传超过10个文件！');
      return;
    }
    console.log('开始转换...');
    simulateApiCall();
  }

  function simulateApiCall() {
    console.log('API调用成功，接收到了压缩包文件');
  }
});