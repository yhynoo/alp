export function cleanTranscription(transcription) {
    const transcriptionArray = transcription
        .split(/\r?\n/) // Split into lines
        .map(line => line
            .replace(/[#()?|\[\]]/g, '')        // Remove special characters
            .replace(/^\d+\S*\s*/, '')          // Remove leading digits and following non-space characters
            .replace(', ', '')                  // Remove remaining comma-space sequences
            .replace(/\.\.\./g, '')             // Remove all occurrences of "..."
            .trim()
        )
        .filter(line => line.trim() !== '');

    return transcriptionArray.join('\n');
}