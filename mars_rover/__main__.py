

from mars_rover.src.layer_coordinator import LayerCoordinator

if __name__ == "__main__":
    input_file_path = "data/basic.txt"  # Replace with your actual input file path
    coordinator = LayerCoordinator(input_file_path)
    coordinator.run()