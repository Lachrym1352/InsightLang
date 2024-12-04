document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById("fileSelect");
    const fileInput = document.getElementById("file-upload");
    const submitButton = form.querySelector("button[type='submit']");
    let isUploading = false; // 요청 중인지 확인하는 플래그
    const fileUpload = document.getElementById('file-upload');
    const uploadLabel = document.getElementById('upload-label');
    const SERVER_URL = document.querySelector('meta[name="server-url"]').getAttribute('content');
    console.log("SERVER_URL:", SERVER_URL);

    // 파일 선택 시 파일 이름 표시
    fileUpload.addEventListener('change', () => {
        if (fileUpload.files.length > 0) {
            const fileName = fileUpload.files[0].name;
            const fileExtension = fileName.split('.').pop().toLowerCase();
            if (fileExtension !== 'pdf') {
                alert("Only PDF files are allowed.");
                fileUpload.value = ""; // 선택된 파일 초기화
                uploadLabel.textContent = "Select Thesis";
                return;
            }
            uploadLabel.textContent = fileName; // 파일 이름 표시
        }
    });

    // 폼 제출 시 서버로 파일 업로드 및 처리
form.addEventListener("submit", async (event) => {
    event.preventDefault(); // 기본 동작 방지

    if (isUploading) {
        alert("File is already being uploaded. Please wait.");
        return;
    }

    if (!fileInput.files.length) {
        alert("Please select a file before uploading.");
        return;
    }

    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append("file", file);

    // 버튼 비활성화 및 요청 상태 설정
    isUploading = true;
    submitButton.disabled = true;
    submitButton.textContent = "Uploading...";

    try {
        const response = await fetch(SERVER_URL, {
            method: "POST",
            body: formData,
        });

        if (response.ok) {
            const data = await response.json();
            console.log("Response:", data);

            // 결과 페이지로 이동
            sessionStorage.setItem("resultData", JSON.stringify(data));
            window.location.href = "result.html";
        } else {
            const error = await response.json();
            console.error("Server Error:", error);
            alert(`Error: ${error.detail || "Unknown server error."}`);
        }
    } catch (err) {
        console.error("Fetch Error:", err);
        alert("A network error occurred while uploading the file. Please try again.");
    } finally {
        // 버튼 활성화 및 요청 상태 초기화
        isUploading = false;
        submitButton.disabled = false;
        submitButton.textContent = "Upload";
    }
});
}
)
