package com.example.websitebackend.model;

import lombok.Data;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.mapping.Field;

@Data
@Document(collection = "insights")
public class Insight {

    @Id
    private String id;

    private String personName;
    private String description;
    private String image;

    @Field("insta_link")
    private String instaLink;

    // Fixed / Styling Data defaults
    private String title = "Insight Series";
    private String bgColor = "rgba(125, 212, 238, 0.15)";
    private String borderColor = "#7dd4ee";
    private String size = "regular";
    private String year = "Alumni";
}