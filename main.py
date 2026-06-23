from process_batch import ProjectInit

if __name__ == "__main__":
    csum            = True

    # --- QRaw Options
    qraw            = True
    qraw_event      = False
    # --- Default qraw_event = False

    # --- Map Plot Options
    mplot           = True
    merge_map_plot  = False
    # --- Default event_map_plot = False
    
    # --- Zip Options
    zip             = True
    map_to_zip      = True
    # --- Default map_to_zip = True
    
    ProjectInit.start_N(
        csum, 
        qraw, 
        qraw_event, 
        mplot, 
        zip, 
        map_to_zip, 
        merge_map_plot
    )