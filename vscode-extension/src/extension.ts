/**
 * Open-SAS VS Code Extension
 * 
 * This extension provides SAS syntax highlighting and execution support
 * for .osas files using the Open-SAS Python backend.
 */

import * as vscode from 'vscode';
import { spawn, ChildProcess } from 'child_process';
import * as path from 'path';
import * as os from 'os';
import { OSASNotebookProvider } from './notebook/osasNotebookProvider';

let outputChannel: vscode.OutputChannel;
let logChannel: vscode.OutputChannel;

export function activate(context: vscode.ExtensionContext) {
    console.log('Open-SAS extension is now active!');
    
    // Create output channels
    outputChannel = vscode.window.createOutputChannel('Open-SAS Output');
    logChannel = vscode.window.createOutputChannel('Open-SAS Log');
    
    // Register commands
    const runFileCommand = vscode.commands.registerCommand('open-sas.runFile', runFile);
    const runSelectionCommand = vscode.commands.registerCommand('open-sas.runSelection', runSelection);
    const checkSyntaxCommand = vscode.commands.registerCommand('open-sas.checkSyntax', checkSyntax);
    
    context.subscriptions.push(runFileCommand, runSelectionCommand, checkSyntaxCommand);
    
    // Register notebook provider
    const notebookProvider = new OSASNotebookProvider();
    const notebookController = vscode.notebooks.createNotebookController(
        'osas-notebook-controller',
        'osas-notebook',
        'Open-SAS'
    );
    
    notebookController.supportedLanguages = ['sas'];
    notebookController.supportsExecutionOrder = true;
    notebookController.executeHandler = (cells, notebook, controller) => {
        for (const cell of cells) {
            notebookProvider.executeCell(notebook, cell);
        }
    };
    
    context.subscriptions.push(notebookController);
    
    // Show output channel on first activation
    outputChannel.show();
}

export function deactivate() {
    // Clean up resources
    if (outputChannel) {
        outputChannel.dispose();
    }
    if (logChannel) {
        logChannel.dispose();
    }
}

/**
 * Run the current .osas file
 */
async function runFile() {
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
        vscode.window.showErrorMessage('No active editor found.');
        return;
    }
    
    const document = editor.document;
    if (!document.fileName.endsWith('.osas')) {
        vscode.window.showErrorMessage('Current file is not a .osas file.');
        return;
    }
    
    // Save the file first
    await document.save();
    
    // Execute the file
    await executeSASFile(document.fileName);
}

/**
 * Run the selected text in the current .osas file
 */
async function runSelection() {
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
        vscode.window.showErrorMessage('No active editor found.');
        return;
    }
    
    const selection = editor.selection;
    if (selection.isEmpty) {
        vscode.window.showErrorMessage('No text selected.');
        return;
    }
    
    const selectedText = editor.document.getText(selection);
    await executeSASText(selectedText);
}

/**
 * Check syntax of the current .osas file
 */
async function checkSyntax() {
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
        vscode.window.showErrorMessage('No active editor found.');
        return;
    }
    
    const document = editor.document;
    if (!document.fileName.endsWith('.osas')) {
        vscode.window.showErrorMessage('Current file is not a .osas file.');
        return;
    }
    
    // For now, just run the file in syntax-check mode
    // In a full implementation, this would parse without executing
    vscode.window.showInformationMessage('Syntax check not yet implemented. Running file instead.');
    await runFile();
}

/**
 * Execute a .osas file
 */
async function executeSASFile(filePath: string) {
    outputChannel.clear();
    outputChannel.appendLine(`Executing: ${filePath}`);
    outputChannel.appendLine('='.repeat(50));
    
    try {
        const pythonPath = await getPythonPath();
        const openSASPath = await getOpenSASPath();
        
        // Spawn Python process to run Open-SAS
        const args = ['-u', openSASPath, filePath];
        const process = spawn(pythonPath, args, {
            cwd: path.dirname(filePath),
            stdio: ['pipe', 'pipe', 'pipe']
        });
        
        await handleProcessOutput(process, filePath);
        
    } catch (error) {
        const errorMessage = `Error executing ${filePath}: ${error}`;
        outputChannel.appendLine(errorMessage);
        vscode.window.showErrorMessage(errorMessage);
    }
}

/**
 * Execute SAS text directly
 */
async function executeSASText(sasText: string) {
    outputChannel.clear();
    outputChannel.appendLine('Executing selected SAS code:');
    outputChannel.appendLine('='.repeat(50));
    
    try {
        const pythonPath = await getPythonPath();
        const openSASPath = await getOpenSASPath();
        
        // Create a temporary file with the selected text
        const tempFile = path.join(os.tmpdir(), `osas_temp_${Date.now()}.osas`);
        require('fs').writeFileSync(tempFile, sasText);
        
        // Spawn Python process
        const args = ['-u', openSASPath, tempFile];
        const process = spawn(pythonPath, args, {
            stdio: ['pipe', 'pipe', 'pipe']
        });
        
        await handleProcessOutput(process, 'Selected Code');
        
        // Clean up temporary file
        require('fs').unlinkSync(tempFile);
        
    } catch (error) {
        const errorMessage = `Error executing SAS code: ${error}`;
        outputChannel.appendLine(errorMessage);
        vscode.window.showErrorMessage(errorMessage);
    }
}

/**
 * Handle process output and errors
 */
async function handleProcessOutput(process: ChildProcess, source: string): Promise<void> {
    return new Promise((resolve, reject) => {
        let hasError = false;
        
        // Handle stdout
        process.stdout?.on('data', (data) => {
            const output = data.toString();
            outputChannel.append(output);
        });
        
        // Handle stderr
        process.stderr?.on('data', (data) => {
            const error = data.toString();
            logChannel.append(`[${source}] ${error}`);
            hasError = true;
        });
        
        // Handle process completion
        process.on('close', (code) => {
            if (code === 0) {
                outputChannel.appendLine(`\nExecution completed successfully.`);
                resolve();
            } else {
                const errorMessage = `Process exited with code ${code}`;
                outputChannel.appendLine(`\n${errorMessage}`);
                if (hasError) {
                    logChannel.show();
                }
                reject(new Error(errorMessage));
            }
        });
        
        // Handle process errors
        process.on('error', (error) => {
            const errorMessage = `Process error: ${error.message}`;
            outputChannel.appendLine(errorMessage);
            reject(error);
        });
        
        // Show output channel
        outputChannel.show();
    });
}

/**
 * Get Python executable path
 */
async function getPythonPath(): Promise<string> {
    const config = vscode.workspace.getConfiguration('open-sas');
    let pythonPath = config.get<string>('pythonPath');
    
    if (!pythonPath) {
        // Try to find Python in common locations
        const pythonCommands = ['python3', 'python'];
        
        for (const cmd of pythonCommands) {
            try {
                await executeCommand(cmd, ['--version']);
                pythonPath = cmd;
                break;
            } catch {
                // Continue to next command
            }
        }
        
        if (!pythonPath) {
            throw new Error('Python not found. Please install Python or set the open-sas.pythonPath setting.');
        }
    }
    
    return pythonPath;
}

/**
 * Get Open-SAS runner script path
 */
async function getOpenSASPath(): Promise<string> {
    const config = vscode.workspace.getConfiguration('open-sas');
    let openSASPath = config.get<string>('openSASPath');
    
    if (!openSASPath) {
        // Try to find Open-SAS in the extension directory
        const extensionPath = vscode.extensions.getExtension('ryan-story.open-sas')?.extensionPath;
        if (extensionPath) {
            const runnerPath = path.join(extensionPath, 'python', 'osas_runner.py');
            if (require('fs').existsSync(runnerPath)) {
                openSASPath = runnerPath;
            }
        }
        
        if (!openSASPath) {
            // Try to use the installed package
            try {
                await executeCommand('python', ['-c', 'import open_sas; print("OK")']);
                openSASPath = 'python -m open_sas.cli';
            } catch {
                throw new Error('Open-SAS not found. Please install the open-sas package or set the open-sas.openSASPath setting.');
            }
        }
    }
    
    return openSASPath;
}

/**
 * Execute a command and return a promise
 */
function executeCommand(command: string, args: string[]): Promise<string> {
    return new Promise((resolve, reject) => {
        const process = spawn(command, args);
        let output = '';
        let error = '';
        
        process.stdout?.on('data', (data) => {
            output += data.toString();
        });
        
        process.stderr?.on('data', (data) => {
            error += data.toString();
        });
        
        process.on('close', (code) => {
            if (code === 0) {
                resolve(output);
            } else {
                reject(new Error(error || `Command failed with code ${code}`));
            }
        });
        
        process.on('error', (err) => {
            reject(err);
        });
    });
}
