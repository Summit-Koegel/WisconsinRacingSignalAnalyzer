import matplotlib.pyplot as plt

def plot_values(df, data_converter):
    for nomenclature, converter_info in data_converter.items():
        signals = converter_info['Signals']
        units = converter_info['Units']
        category = converter_info['Category']
        priority = converter_info['Priority']
        
        # Plot each signal
        for signal in signals:
            if signal in df.columns:
                plt.figure(figsize=(10, 6))
                plt.plot(df['t'], df[signal], label=f"{nomenclature} ({units})")
                plt.title(f"{nomenclature} ({category}) - Priority {priority}")
                plt.xlabel('Time')
                plt.ylabel('Value')
                plt.legend()
                plt.grid(True)
                plt.show()
                

                
