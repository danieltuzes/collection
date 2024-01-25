const app = new Vue({
    el: '#app',
    data: {
        files: [],
        selectedFile: null,
        isLoading: false
    },
    methods: {
        submitForm() {
            this.isLoading = true;

            const formData = new FormData(document.getElementById('upload-form'));
            fetch('/process-csv', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                this.files.push(data.output_filename);
                this.files.sort();
                this.isLoading = false;
            })
            .catch(error => {
                console.error('Error processing the file:', error);
                this.isLoading = false;
            });
        }
    }
});