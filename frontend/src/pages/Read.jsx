// src/pages/Read.jsx
export default function Read() {
    return (
        <div>
            <h1>Immersion Hub: Read</h1>
            <p>Upload a local .epub file below to start reading.</p>
            <input type="file" accept=".epub" />
            <div style={{ marginTop: '2rem', padding: '2rem', border: '1px dashed #ccc' }}>
                EPUB Canvas will render here...
            </div>
        </div>
    );
}