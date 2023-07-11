package main

import (
	"fmt"
	"os"
	"os/exec"
	"strings"

	"gopkg.in/yaml.v2"
)

type Package struct {
	Name    string `yaml:"name"`
	Version string `yaml:"version"`
	Epoch   int    `yaml:"epoch"`
}

type Document struct {
	Package Package `yaml:"package"`
}

func main() {
	// get changed files
	out, err := exec.Command("git", "diff", "--name-only", "origin/main...HEAD").Output()
	if err != nil {
		fmt.Println("Failed to get changed files")
		os.Exit(1)
	}

	files := strings.Split(string(out), "\n")

	for _, file := range files {
		if strings.HasSuffix(file, ".yaml") {
			checkEpochIncrement(file)
		}
	}
}

func checkEpochIncrement(filename string) {
	oldContent, _ := exec.Command("git", "show", fmt.Sprintf("origin/main:%s", filename)).Output()
	newContent, _ := exec.Command("git", "show", fmt.Sprintf("HEAD:%s", filename)).Output()

	var oldDoc, newDoc Document

	err := yaml.Unmarshal(oldContent, &oldDoc)
	if err != nil {
		fmt.Printf("Error parsing YAML file: %s\n", err)
		os.Exit(1)
	}

	err = yaml.Unmarshal(newContent, &newDoc)
	if err != nil {
		fmt.Printf("Error parsing YAML file: %s\n", err)
		os.Exit(1)
	}

	if oldDoc.Package.Version != newDoc.Package.Version {
		// If the version has changed, we don't require the epoch to be incremented
		return
	}

	if oldDoc.Package.Epoch+1 != newDoc.Package.Epoch {
		fmt.Printf("The package.epoch in %s should probably be incremented by one.\n", filename)
		os.Exit(1)
	}
}

