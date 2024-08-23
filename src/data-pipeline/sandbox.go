package main

import (
	"fmt"

	"github.com/airbusgeo/godal"
)

func main() {
	godal.RegisterAll()
	filename := "/workspace/data/landsat-8/LC09_L2SP_044034_20240812_20240813_02_T1/LC09_L2SP_044034_20240812_20240813_02_T1_QA_PIXEL.TIF"

	// Open raster dataset
	hDS, err := godal.Open(filename)
	if err != nil {
		panic(err)
	}

	// Get structure
	structure := hDS.Structure()
	fmt.Printf("dataset size: %dx%dx%d\n", structure.SizeX, structure.SizeY, structure.NBands)
	for _, band := range hDS.Bands() {
		for o, ovr := range band.Overviews() {
			bstruct := ovr.Structure()
			fmt.Printf("overview %d size: %dx%d\n", o, bstruct.SizeX, bstruct.SizeY)
		}
	}
}
