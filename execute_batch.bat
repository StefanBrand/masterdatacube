@echo off
for /f "delims=" %%b in (bounds.txt) DO (
    docker run -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY -v %CD%:/mnt/ registry.gitlab.eox.at/maps/mapchete_hub/mhub:0.10 mhub -h demo-m.hub.eox.at execute /mnt/datacubes.mapchete -b %%b --queue masterdatacube_queue
)