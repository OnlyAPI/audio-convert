var API_BASE_URL = 'http://localhost:8081/py-api'; // 开发环境
// var API_BASE_URL = 'https://devpy.zhengzai.tv/py-api'; // 生产环境

function apiRequest(path, options = {}) {
  const url = `${API_BASE_URL}${path}`;
  return fetch(url, options)
    .then(response => {
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return response.json();
    })
    .catch(error => {
      console.error('API请求失败:', error);
      throw error;
    });
}

// 修改开始转换按钮
function change_start_conversion_button(status) {
  const button = document.getElementById('startConversion');
  button.disabled = status;
}


// 用于显示提示消息
function showNotification(message, type = 'success') {
  const notificationContainer = document.getElementById('notificationContainer');
  
  const notification = document.createElement('div');
  notification.className = `notification ${type}`;
  notification.textContent = message;

  notificationContainer.appendChild(notification);
  
  // 延迟显示，增加显示动画效果
  setTimeout(() => {
    notification.classList.add('show');
  }, 150);

  // 1秒后自动消失并移除提示框
  setTimeout(() => {
    notification.classList.remove('show');
    setTimeout(() => notification.remove(), 300); // 等待动画完成后移除元素
  }, 2000); // 1秒后消失
}



function initAudioConverter() {
  const navLinks = document.querySelectorAll('.nav a');
  const contents = document.querySelectorAll('.content');
  const fileInput = document.getElementById('fileInput');
  const uploadArea = document.getElementById('uploadArea');
  const filesList = document.getElementById('filesList');
  const addFilesButton = document.getElementById('addFiles');
  const clearFilesButton = document.getElementById('clearFiles');
  const formatOptionsContainer = document.getElementById('formatOptions');
  const startConversionButton = document.getElementById('startConversion');
  
  // 用于保存当前选择的文件
  let selectedFiles = [];

  // 动态获取音频格式选项
  fetchAudioFormats();
  fetchReceiveAudioFormats()

  
   // 获取支持的目标音频格式
  function fetchAudioFormats() {
    apiRequest('/support/target-audio')
      .then(response => response)
      .then(data => {
        generateFormatOptions(data.data);
      })
      .catch(error => {
        console.error('获取音频格式失败:', error);
      });
  }


  // 获取支持的输入音频格式
  function fetchReceiveAudioFormats() {
    apiRequest('/support/receive-audio')
      .then(response => response)
      .then(data => {
          // 将接口返回的格式拼接成字符串：.mp3,.mov,.wav
          const acceptValue = data.data.map(format => `.${format}`).join(',');
          fileInput.setAttribute('accept', acceptValue);
          console.log('Updated accept attribute to:', acceptValue);
      })
      .catch(error => {
        console.error('获取音频格式失败:', error);
      });
  }

  function generateFormatOptions(audioFormats) {
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

  }

  // 事件绑定
  navLinks.forEach(link => {
    link.addEventListener('click', switchContent);
  });

  addFilesButton.addEventListener('click', () => fileInput.click());
  clearFilesButton.addEventListener('click', clearFiles);
  uploadArea.addEventListener('dragover', e => e.preventDefault());
  uploadArea.addEventListener('drop', handleDrop);
  fileInput.addEventListener('change', handleFiles);
  startConversionButton.addEventListener('click', startConversionProcess);

  // 切换内容
  function switchContent(e) {
    e.preventDefault();
    const targetTab = e.target.getAttribute('data-tab');
    contents.forEach(content => content.classList.remove('active'));
    document.getElementById(targetTab).classList.add('active');
    navLinks.forEach(navLink => navLink.classList.remove('active'));
    e.target.classList.add('active');
  }

  // 文件处理
  function handleFiles(e) {
    const newFiles = Array.from(e.target.files);  // 保存当前选择的新文件
    selectedFiles = [...selectedFiles, ...newFiles];  // 合并新文件与已选文件
    updateFileList();
  }


  function handleDrop(e) {
    e.preventDefault();
    const newFiles = Array.from(e.dataTransfer.files);  // 保存拖拽的新文件
    selectedFiles = [...selectedFiles, ...newFiles];  // 合并新文件与已选文件
    updateFileList();
  }


  // 更新文件列表显示
  function updateFileList() {
    clearFilesList();  // 清空列表
    selectedFiles.forEach((file, index) => {
      const li = document.createElement('li');
      li.textContent = file.name;
      const removeBtn = document.createElement('button');
      removeBtn.textContent = '删除';
      removeBtn.onclick = () => {
        removeFile(index);  // 删除指定文件
      };
      li.appendChild(removeBtn);
      filesList.appendChild(li);
    });
  }


  // 隐藏选择文件后的删除按钮
  function hideRemoveButton(){
    const buttons = document.querySelectorAll('#filesList button');
    buttons.forEach(button => {
        button.style.visibility = 'hidden'; // 隐藏按钮但保留占位
    });
  }


  // 删除文件
  function removeFile(index) {
    selectedFiles.splice(index, 1);  // 从文件列表中移除文件
    updateFileList();  // 更新显示
  }

  // 清空文件列表显示
  function clearFilesList() {
    while (filesList.firstChild) {
      filesList.removeChild(filesList.firstChild);
    }
  }

  // 清空文件
  function clearFiles() {
    selectedFiles = [];  // 清空文件数组
    clearFilesList();    // 清空文件列表显示
  }

  // 开始转换
  function startConversionProcess() {
    if (selectedFiles.length === 0) {
      // 示例调用
      showNotification('选择要转换的文件', 'warning');
      return;
    }

    const selectedFormat = document.querySelector('input[name="outputFormat"]:checked');
    if (!selectedFormat) {
      showNotification('先选择输出格式', 'warning');
      return;
    }

    if (selectedFiles.length > 10) {
      showNotification('不能超过10个文件', 'warning');
      return;
    }
    hideRemoveButton()
    change_start_conversion_button(true);

    const formData = new FormData();
    selectedFiles.forEach(file => formData.append('files', file));  // 使用selectedFiles而不是fileInput
    formData.append('targetType', selectedFormat.value);

    // 发送POST请求
    fetch(API_BASE_URL + '/convert/audio', {
      method: 'POST',
      body: formData
    })
    .then(response => {
      if (!response.ok) {
        return response.json().then(data => {
          throw new Error(data.error || '请求失败，请稍后再试。');
        });
      }
      return response.blob().then(blob => ({ blob, response }));
    })
    .then(({ blob, response }) => {
      if (response.status === 200) {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = 'converted.zip'; // 指定下载文件名
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url); // 释放 URL
        showNotification('转换成功，请查看下载文件!', 'success');
      }
      clearFiles();  // 清空文件
      change_start_conversion_button(false);
    })
    .catch(error => {
      console.error('Error:', error);
      clearFiles();  // 清空文件
      showNotification('转换失败，请稍后再试', 'error');
      change_start_conversion_button(false);
    });
  }
}

// 初始化音频转换工具
initAudioConverter();
