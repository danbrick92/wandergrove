package main

import (
	"fmt"
	"io"
	"net/http"
	"os"
	"time"

	"path/filepath"
)

// const url string = "https://zenodo.org/record/20546682/files/interactions.tsv.gz"
const url string = "https://zenodo.org/records/18220953/files/SInAS_3.1.1.csv?download=1"
const source = "globi"
const fileName = "SInAS_3.1.1.csv"
const newFileDirMode = 0775

func getBaseDirectory() string {
	return filepath.Join("/", "Users", "danielbrickner", "data")
}

func getFile(url string, path string) {
	out, err := os.Create(path)
	if err != nil {
		panic("dis ting broke mon")
	}
	defer out.Close()

	resp, err := http.Get(url)
	if err != nil {
		panic("Could not download")
	}
	defer resp.Body.Close()

	if resp.StatusCode == http.StatusOK {
		bodyBytes, err := io.ReadAll(resp.Body)
		if err != nil {
			panic(err)
		}
		os.WriteFile(path, bodyBytes, newFileDirMode)
	}
}

func getParentDownloadPath(basePath string) string {
	t := time.Now().UTC()
	dt := t.Format(time.RFC3339)
	return filepath.Join(basePath, source, dt)
}

func getDownloadPath(parentPath string) string {
	return filepath.Join(parentPath, fileName)
}

func makeParentDirectory(parentPath string) {
	os.MkdirAll(parentPath, newFileDirMode)
}

func blah() {
	baseDirectory := getBaseDirectory()
	parentDirectory := getParentDownloadPath(baseDirectory)
	makeParentDirectory(parentDirectory)
	downloadPath := getDownloadPath(parentDirectory)
	fmt.Println(downloadPath)
	getFile(url, downloadPath)
}
