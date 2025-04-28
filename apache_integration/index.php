<?php
// Serve React static build properly

$static_build_path = realpath(__DIR__ . '/frontend');

// Stop if missing
if ($static_build_path === false) {
    http_response_code(500);
    echo "<h1>500 Internal Server Error</h1><p>Static frontend build not found.</p>";
    exit;
}

// Sanitize
$request_uri = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
$request_uri = str_replace('..', '', $request_uri);

// Special case for root or index
if ($request_uri === '/' || $request_uri === '/index.php') {
    $request_uri = '/index.html';
}

// Build full path
$requested_file = realpath($static_build_path . $request_uri);

// Serve static file if exists
if ($requested_file !== false && strpos($requested_file, $static_build_path) === 0 && is_file($requested_file)) {
    $mime_type = mime_content_type($requested_file) ?: 'application/octet-stream';
    header('Content-Type: ' . $mime_type);
    header('Content-Length: ' . filesize($requested_file));
    readfile($requested_file);
    exit;
}

// Otherwise fallback to React index.html
$index_file = $static_build_path . '/index.html';
if (file_exists($index_file)) {
    header('Content-Type: text/html');
    header('Content-Length: ' . filesize($index_file));
    readfile($index_file);
    exit;
}

// 404 fallback
http_response_code(404);
echo "<h1>404 Not Found</h1><p>React build not found.</p>";
exit;
?>
