"use strict";
/**
 * Open-SAS Notebook Renderer
 *
 * This module provides custom rendering for Open-SAS notebook outputs,
 * including datasets, PROC results, and other SAS-specific content.
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.OSASNotebookRenderer = void 0;
class OSASNotebookRenderer {
    constructor(context) {
        this.context = context;
    }
    render(outputItem, element) {
        const mimeType = outputItem.mime;
        const data = outputItem.data;
        switch (mimeType) {
            case 'text/x-sas-output':
                this.renderSASOutput(data, element);
                break;
            case 'text/x-sas-error':
                this.renderSASError(data, element);
                break;
            case 'application/vnd.sas.dataset':
                this.renderDataset(data, element);
                break;
            case 'text/html':
                this.renderHTML(data, element);
                break;
            default:
                this.renderText(data, element);
        }
    }
    renderSASOutput(data, element) {
        const div = document.createElement('div');
        div.className = 'sas-output';
        div.style.cssText = `
            font-family: 'Courier New', monospace;
            font-size: 12px;
            line-height: 1.4;
            background-color: #f8f8f8;
            border: 1px solid #ddd;
            border-radius: 4px;
            padding: 10px;
            margin: 5px 0;
            white-space: pre-wrap;
            overflow-x: auto;
        `;
        // Format SAS output with syntax highlighting
        const formattedData = this.formatSASOutput(data);
        div.innerHTML = formattedData;
        element.appendChild(div);
    }
    renderSASError(data, element) {
        const div = document.createElement('div');
        div.className = 'sas-error';
        div.style.cssText = `
            font-family: 'Courier New', monospace;
            font-size: 12px;
            line-height: 1.4;
            background-color: #ffe6e6;
            border: 1px solid #ff9999;
            border-radius: 4px;
            padding: 10px;
            margin: 5px 0;
            white-space: pre-wrap;
            color: #cc0000;
        `;
        div.textContent = data;
        element.appendChild(div);
    }
    renderDataset(data, element) {
        const div = document.createElement('div');
        div.className = 'sas-dataset';
        div.style.cssText = `
            margin: 10px 0;
            border: 1px solid #ddd;
            border-radius: 4px;
            padding: 10px;
            font-family: Arial, sans-serif;
        `;
        if (data && data.name) {
            const header = document.createElement('h4');
            header.textContent = `Dataset: ${data.name}`;
            header.style.cssText = 'margin: 0 0 10px 0; color: #333;';
            div.appendChild(header);
            const info = document.createElement('p');
            info.textContent = `${data.shape[0]} observations, ${data.shape[1]} variables`;
            info.style.cssText = 'margin: 0 0 10px 0; color: #666; font-size: 0.9em;';
            div.appendChild(info);
            if (data.head && data.head.length > 0) {
                const table = this.createDatasetTable(data.head, data.columns);
                div.appendChild(table);
            }
        }
        element.appendChild(div);
    }
    renderHTML(data, element) {
        const div = document.createElement('div');
        div.innerHTML = data;
        element.appendChild(div);
    }
    renderText(data, element) {
        const div = document.createElement('div');
        div.style.cssText = `
            font-family: 'Courier New', monospace;
            font-size: 12px;
            line-height: 1.4;
            white-space: pre-wrap;
            margin: 5px 0;
        `;
        div.textContent = data;
        element.appendChild(div);
    }
    formatSASOutput(data) {
        // Add basic syntax highlighting for SAS output
        return data
            .replace(/ERROR:/g, '<span style="color: #cc0000; font-weight: bold;">ERROR:</span>')
            .replace(/WARNING:/g, '<span style="color: #ff6600; font-weight: bold;">WARNING:</span>')
            .replace(/NOTE:/g, '<span style="color: #0066cc; font-weight: bold;">NOTE:</span>')
            .replace(/PROC\s+(\w+)/gi, '<span style="color: #0066cc; font-weight: bold;">PROC $1</span>')
            .replace(/DATA\s+(\w+)/gi, '<span style="color: #0066cc; font-weight: bold;">DATA $1</span>');
    }
    createDatasetTable(head, columns) {
        const table = document.createElement('table');
        table.style.cssText = `
            border-collapse: collapse;
            width: 100%;
            font-size: 0.9em;
            margin-top: 10px;
        `;
        // Create header
        const thead = document.createElement('thead');
        const headerRow = document.createElement('tr');
        headerRow.style.cssText = 'background-color: #f5f5f5;';
        columns.forEach(col => {
            const th = document.createElement('th');
            th.textContent = col;
            th.style.cssText = 'border: 1px solid #ddd; padding: 8px; text-align: left; font-weight: bold;';
            headerRow.appendChild(th);
        });
        thead.appendChild(headerRow);
        table.appendChild(thead);
        // Create body
        const tbody = document.createElement('tbody');
        head.forEach(row => {
            const tr = document.createElement('tr');
            columns.forEach(col => {
                const td = document.createElement('td');
                td.textContent = row[col] || '';
                td.style.cssText = 'border: 1px solid #ddd; padding: 8px;';
                tr.appendChild(td);
            });
            tbody.appendChild(tr);
        });
        table.appendChild(tbody);
        return table;
    }
}
exports.OSASNotebookRenderer = OSASNotebookRenderer;
//# sourceMappingURL=renderer.js.map