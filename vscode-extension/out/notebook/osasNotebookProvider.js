"use strict";
/**
 * Open-SAS Notebook Provider for VS Code
 *
 * This module provides notebook support for Open-SAS,
 * allowing interactive execution of SAS code in VS Code notebooks.
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.OSASNotebookProvider = void 0;
const vscode = require("vscode");
const child_process_1 = require("child_process");
const path = require("path");
class OSASNotebookProvider {
    constructor() {
        this.interpreters = new Map();
        this.outputChannel = vscode.window.createOutputChannel('Open-SAS Notebook');
    }
    async resolveNotebook(document, webview) {
        // Initialize notebook communication
        this.outputChannel.appendLine(`Resolved notebook: ${document.uri.fsPath}`);
    }
    async executeCell(document, cell) {
        const sasCode = cell.document.getText();
        if (!sasCode.trim()) {
            // Empty cell
            cell.outputs = [];
            return;
        }
        try {
            // Execute SAS code
            const result = await this.executeSASCode(sasCode, document.uri.fsPath);
            // Create output items
            const outputItems = [];
            // Add text output
            if (result.output) {
                outputItems.push(vscode.NotebookCellOutputItem.text(result.output, 'text/x-sas-output'));
            }
            // Add error output
            if (result.errors) {
                outputItems.push(vscode.NotebookCellOutputItem.text(result.errors, 'text/x-sas-error'));
            }
            // Add dataset displays
            if (result.datasets) {
                for (const [name, dataset] of Object.entries(result.datasets)) {
                    const html = this.createDatasetHTML(name, dataset);
                    outputItems.push(vscode.NotebookCellOutputItem.text(html, 'text/html'));
                }
            }
            // Add PROC results
            if (result.proc_results) {
                for (const procResult of result.proc_results) {
                    const html = this.createPROCResultHTML(procResult);
                    outputItems.push(vscode.NotebookCellOutputItem.text(html, 'text/html'));
                }
            }
            // Update cell output
            if (outputItems.length > 0) {
                cell.outputs = [new vscode.NotebookCellOutput(outputItems)];
            }
            else {
                cell.outputs = [];
            }
        }
        catch (error) {
            // Handle execution error
            const errorOutput = new vscode.NotebookCellOutput([
                vscode.NotebookCellOutputItem.text(`Error executing SAS code: ${error}`, 'text/x-sas-error')
            ]);
            cell.outputs = [errorOutput];
        }
    }
    async executeSASCode(code, notebookPath) {
        return new Promise((resolve, reject) => {
            const pythonPath = this.getPythonPath();
            const scriptPath = path.join(__dirname, '..', '..', 'python', 'notebook_runner.py');
            const process = (0, child_process_1.spawn)(pythonPath, [scriptPath, '--code', code, '--notebook', notebookPath], {
                cwd: path.dirname(notebookPath),
                stdio: ['pipe', 'pipe', 'pipe']
            });
            let output = '';
            let error = '';
            process.stdout.on('data', (data) => {
                output += data.toString();
            });
            process.stderr.on('data', (data) => {
                error += data.toString();
            });
            process.on('close', (code) => {
                if (code === 0) {
                    try {
                        const result = JSON.parse(output);
                        resolve(result);
                    }
                    catch (e) {
                        resolve({
                            output: output,
                            errors: error,
                            datasets: {},
                            proc_results: []
                        });
                    }
                }
                else {
                    reject(new Error(`Process exited with code ${code}: ${error}`));
                }
            });
            process.on('error', (err) => {
                reject(err);
            });
        });
    }
    getPythonPath() {
        const config = vscode.workspace.getConfiguration('open-sas');
        return config.get('pythonPath') || 'python';
    }
    createDatasetHTML(name, dataset) {
        const { shape, columns, head } = dataset;
        let html = `
            <div class="sas-dataset" style="margin: 10px 0; border: 1px solid #ddd; border-radius: 4px; padding: 10px; font-family: monospace;">
                <h4 style="margin: 0 0 10px 0; color: #333;">Dataset: ${name}</h4>
                <p style="margin: 0 0 10px 0; color: #666; font-size: 0.9em;">
                    ${shape[0]} observations, ${shape[1]} variables
                </p>
        `;
        if (head && head.length > 0) {
            html += `
                <table style="border-collapse: collapse; width: 100%; font-size: 0.9em;">
                    <thead>
                        <tr style="background-color: #f5f5f5;">
                            ${columns.map((col) => `<th style="border: 1px solid #ddd; padding: 8px; text-align: left;">${col}</th>`).join('')}
                        </tr>
                    </thead>
                    <tbody>
                        ${head.map((row) => `<tr>${columns.map((col) => `<td style="border: 1px solid #ddd; padding: 8px;">${row[col] || ''}</td>`).join('')}</tr>`).join('')}
                    </tbody>
                </table>
            `;
        }
        html += '</div>';
        return html;
    }
    createPROCResultHTML(procResult) {
        // Create HTML for PROC results
        let html = `
            <div class="sas-proc-result" style="margin: 10px 0; border: 1px solid #ddd; border-radius: 4px; padding: 10px;">
                <h4 style="margin: 0 0 10px 0; color: #333;">${procResult.proc_name} Results</h4>
        `;
        if (procResult.data) {
            html += `
                <table style="border-collapse: collapse; width: 100%; font-size: 0.9em;">
                    <tbody>
                        ${procResult.data.map((row) => `<tr>${Object.values(row).map((val) => `<td style="border: 1px solid #ddd; padding: 8px;">${val}</td>`).join('')}</tr>`).join('')}
                    </tbody>
                </table>
            `;
        }
        html += '</div>';
        return html;
    }
}
exports.OSASNotebookProvider = OSASNotebookProvider;
//# sourceMappingURL=osasNotebookProvider.js.map