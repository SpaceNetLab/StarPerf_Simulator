# Visualization Setup

This page provides detailed setup instructions for StarPerf's visualization capabilities.

## Quick Setup

For a quick start with visualization:

```bash
# 1. Install Node.js and http-server
npm install -g http-server

# 2. Configure your Cesium token in visualization/html_head_tail/head.html

# 3. Generate visualization in your script
uv run python StarPerf.py  # With visualization code uncommented

# 4. Start the server
cd visualization/CesiumAPP
http-server -p 8081

# 5. Open browser to http://127.0.0.1:8081/<your-file>.html
```

## Detailed Configuration

### Cesium Ion Access Token

1. Visit [Cesium Ion](https://cesium.com/ion/)
2. Create a free account or sign in
3. Navigate to "Access Tokens" in your dashboard
4. Copy your default token or create a new one
5. Paste it in `visualization/html_head_tail/head.html`:

```javascript
// In head.html
Cesium.Ion.defaultAccessToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...';
```

### Directory Structure

The visualization module uses the following structure:

```
visualization/
├── constellation_visualization.py   # Main visualization module
├── CesiumAPP/                      # Generated HTML files
│   └── [generated_files].html
├── html_head_tail/                 # HTML templates
│   ├── head.html                   # Header with Cesium config
│   └── tail.html                   # Footer template
└── samples/                        # Example scripts
    ├── Starlink.py
    ├── OneWeb.py
    ├── Telesat.py
    ├── Boeing.py
    └── visualization_test_cases.py
```

### Node.js Version Management

If you have multiple Node.js versions, use nvm (Node Version Manager):

```bash
# Install nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

# Install Node.js 18
nvm install 18
nvm use 18

# Install http-server
npm install -g http-server
```

## Advanced Configuration

### Custom HTML Templates

You can customize the visualization appearance by modifying the templates:

**head.html** - Controls:
- Cesium library imports
- Initial camera position
- Globe appearance
- Lighting settings

**tail.html** - Controls:
- UI controls
- Animation controls
- Information panels

### Server Configuration

#### Custom Port

```bash
http-server -p 3000
```

#### Enable CORS

```bash
http-server --cors
```

#### Cache Control

```bash
http-server -c-1  # Disable caching
```

#### Bind to All Interfaces

```bash
http-server -a 0.0.0.0 -p 8081
```

This allows access from other devices on your network at:
```
http://<your-ip>:8081/<filename>.html
```

### Production Deployment

For production deployment, consider using:

**Nginx Configuration:**
```nginx
server {
    listen 80;
    server_name your-domain.com;
    root /path/to/StarPerf_Simulator/visualization/CesiumAPP;

    location / {
        try_files $uri $uri/ =404;
    }
}
```

**Apache Configuration:**
```apache
<VirtualHost *:80>
    ServerName your-domain.com
    DocumentRoot /path/to/StarPerf_Simulator/visualization/CesiumAPP

    <Directory /path/to/StarPerf_Simulator/visualization/CesiumAPP>
        Options Indexes FollowSymLinks
        AllowOverride None
        Require all granted
    </Directory>
</VirtualHost>
```

## Visualization API

### Basic Usage

```python
from visualization import constellation_visualization

# Generate visualization
constellation_visualization.visualize_constellation(
    constellation=my_constellation,
    output_dir="./visualization/CesiumAPP",
    filename="my_viz.html"
)
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `constellation` | Constellation | Required | Constellation object to visualize |
| `output_dir` | str | `"./visualization/CesiumAPP"` | Output directory for HTML |
| `filename` | str | `"visualization.html"` | Output filename |
| `show_orbits` | bool | `True` | Display orbital paths |
| `show_isls` | bool | `False` | Show inter-satellite links |
| `show_ground_stations` | bool | `True` | Display ground stations |
| `satellite_color` | str | `"cyan"` | Satellite marker color |
| `orbit_color` | str | `"white"` | Orbital path color |
| `animation_speed` | float | `1.0` | Animation speed multiplier |
| `start_time` | str | `None` | Start time (ISO 8601 format) |
| `duration` | int | `None` | Duration in seconds |

### Example with All Parameters

```python
constellation_visualization.visualize_constellation(
    constellation=starlink_constellation,
    output_dir="./visualization/CesiumAPP",
    filename="starlink_full.html",
    show_orbits=True,
    show_isls=True,
    show_ground_stations=True,
    satellite_color="yellow",
    orbit_color="rgba(255,255,255,0.3)",
    animation_speed=2.0,
    start_time="2024-01-01T00:00:00Z",
    duration=86400  # 24 hours
)
```

## Troubleshooting Guide

### Issue: Blank Page

**Symptoms**: Browser shows blank page with no errors

**Solutions**:
1. Check browser console (F12) for JavaScript errors
2. Verify Cesium token is valid
3. Ensure HTML file was generated correctly
4. Check if WebGL is enabled in browser

### Issue: Slow Performance

**Symptoms**: Laggy visualization, low frame rate

**Solutions**:
1. Reduce number of visible satellites (filter by shell)
2. Disable ISL visualization if not needed
3. Lower animation speed
4. Enable hardware acceleration in browser
5. Use a more powerful GPU

### Issue: Satellites Not Appearing

**Symptoms**: Globe loads but no satellites visible

**Solutions**:
1. Check that constellation data was loaded successfully
2. Verify satellite positions are being generated
3. Zoom out to ensure satellites are in view
4. Check JavaScript console for errors

### Issue: Server Won't Start

**Symptoms**: `http-server` command fails or port in use

**Solutions**:
```bash
# Check if port is in use
lsof -i :8081

# Kill process using port
kill -9 <PID>

# Or use different port
http-server -p 8082
```

## Tips and Best Practices

### Performance Optimization

1. **Limit Visible Satellites**: Visualize one shell at a time for large constellations
2. **Reduce Animation Speed**: Lower speeds reduce computational load
3. **Disable Unnecessary Features**: Turn off ISLs if not analyzing connectivity
4. **Use Modern Browser**: Chrome/Chromium typically has best performance

### Visual Quality

1. **Camera Position**: Start with a good initial camera angle
2. **Color Scheme**: Use contrasting colors for different elements
3. **Lighting**: Adjust ambient and directional lighting for clarity
4. **Orbit Trails**: Show orbit trails to visualize satellite paths

### Workflow Integration

1. **Generate During Simulation**: Create visualization as part of your analysis pipeline
2. **Version Control**: Save visualizations with meaningful filenames
3. **Documentation**: Include screenshots in reports
4. **Sharing**: Deploy to web server for team collaboration

## Next Steps

- Return to [Constellation Visualization](./constellation.md) for usage examples
- Explore [Examples](../examples/overview.md) for complete workflows
- Learn about [Constellation Generation](../core-modules/constellation-generation/overview.md)
