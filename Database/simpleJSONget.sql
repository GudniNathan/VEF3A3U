DROP FUNCTION IF EXISTS courseJSON;
DELIMITER //

CREATE FUNCTION courseJSON() RETURNS TEXT
BEGIN
    DECLARE j JSON;
	DECLARE v_finished INTEGER DEFAULT 0;
    DECLARE courseInfo JSON;
	DECLARE cur_course char(11);
    DECLARE restrictor char(11);
	DECLARE res_type char(1);
    DECLARE res_obj json;
    DECLARE restrictorArray json;

    	
	DEClARE course_cursor CURSOR FOR 
		SELECT courseNumber FROM Courses;
	
	DEClARE restrictor_cursor CURSOR FOR 
		SELECT restrictorID, restrictorType FROM Restrictors
			WHERE courseNumber = cur_course;
        
		-- declare NOT FOUND handler
	DECLARE CONTINUE HANDLER 
		FOR NOT FOUND SET v_finished = 1;
	
    
    SET j = JSON_ARRAY();
    
	OPEN course_cursor;
		courses_loop: LOOP
                
			FETCH course_cursor INTO cur_course;     
            

            					
			IF v_finished = 1 THEN 
				LEAVE courses_loop;
			END IF;
            
			SET restrictorArray = JSON_ARRAY();
            
            
			OPEN restrictor_cursor;
				restrictor_loop: LOOP
                
					FETCH restrictor_cursor INTO restrictor, res_type;                    
					
					IF v_finished = 1 THEN 
						SET v_finished = 0;
						LEAVE restrictor_loop;
					END IF;
                    SET res_obj = JSON_OBJECT('id', restrictor, 'type', res_type);
                    
                    SET restrictorArray = JSON_ARRAY_APPEND(restrictorArray, '$', res_obj);
                    
				END LOOP restrictor_loop;
			CLOSE restrictor_cursor;
            
			SET j = JSON_ARRAY_APPEND(j, '$', JSON_OBJECT('id', cur_course, 'precursors', restrictorArray));                                        
		END LOOP courses_loop;
	CLOSE course_cursor;
    RETURN(JSON_UNQUOTE(j));
END//

DELIMITER ;

SELECT courseJSON();
