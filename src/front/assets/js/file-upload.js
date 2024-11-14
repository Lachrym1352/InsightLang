document.addEventListener('DOMContentLoaded', function() {
    const fileUpload = document.getElementById('file-upload');
    const uploadLabel = document.getElementById('upload-label');

    // 파일 선택 시 파일 이름 표시
    fileUpload.addEventListener('change', () => {
        if (fileUpload.files.length > 0) {
            uploadLabel.textContent = fileUpload.files[0].name; // 선택한 파일 이름을 라벨에 표시
        }
    });
});
