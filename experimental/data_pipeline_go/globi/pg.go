package main

import (
	"encoding/csv"
	"fmt"
	"io"
	"os"
	"path/filepath"
	"time"
)

func findFile() string {
	baseDirectory := getBaseDirectory()
	sourceDirectory := filepath.Join(baseDirectory, source)

	entries, err := os.ReadDir(sourceDirectory)
	if err != nil {
		panic(err)
	}

	var latestFolder string
	var latestTime time.Time

	for _, entry := range entries {
		if !entry.IsDir() {
			continue
		}

		info, err := entry.Info()
		if err != nil {
			panic(err)
		}

		if info.ModTime().After(latestTime) {
			latestTime = info.ModTime()
			latestFolder = filepath.Join(sourceDirectory, entry.Name())
		}
	}

	fileToOpen := filepath.Join(latestFolder, fileName)
	_, err = os.Stat(fileToOpen)
	if err != nil {
		panic("no file found mon")
	}
	return fileToOpen
}

func processRow(ch chan string) {

}

func readCsv(filepath string) {
	startTime := time.Now()
	file, err := os.Open(filepath)
	if err != nil {
		panic("cannot open file")
	}
	defer file.Close()

	reader := csv.NewReader(file)
	reader.Comma = ' '
	reader.LazyQuotes = true

	for {
		_, err := reader.Read()
		if err == io.EOF {
			break
		}
		if err != nil {
			panic(err)
		}
	}
	fmt.Println(time.Since(startTime))

	ch := make(chan string)

}

func main() {
	filePath := findFile()
	fmt.Println(filePath)
	readCsv(filePath)
}
