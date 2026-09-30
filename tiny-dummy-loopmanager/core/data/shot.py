from laplace_log import log


class Shot:
    def __init__(self, shot_number: int):
        self.motors = {}  # rack_address -> {index: MotorInfo}
        self.shot_number = shot_number
        self._raw_master_data = None

    def __repr__(self):
        rack_count = len(self.motors)
        total_motors = sum(len(indices) for indices in self.motors.values())
        
        # Get diagnostic count (assuming stored somewhere, e.g., self.diagnostics)
        diag_count = getattr(self, 'diagnostics', None)
        diag_count = len(diag_count) if diag_count else 0
        
        return (
            f"<Shot shot={self.shot_number} "
            f"racks={rack_count} motors={total_motors} "
            f"diagnostics={diag_count}>")
        
    
    # =========================================================================
    #               CONSTRUCTOR / FACTORY
    # =========================================================================
    
    @classmethod
    def from_master_data(cls, master_data: dict) -> 'Shot | None':
        """
        Factory method: construct Shot from raw Master output.
        Returns None if parsing fails.
        """
        # Step 1: Extract all shot numbers from devices
        device_shot_numbers = cls._collect_device_shot_numbers(master_data)
        log.info(f'device_shot_numbers: {device_shot_numbers}')

        # Step 2: Verify congruence across devices
        try:
            unified_shot_number = cls._verify_shot_congruence(device_shot_numbers)
        except Exception as e:
            unified_shot_number = None
            log.error(f'Exception: {e}')
        
        
        if unified_shot_number is None:
            log.warning(f"Shot number incongruence detected: {device_shot_numbers}")
            # Decide: fail silently, raise, or pick first with warning
            unified_shot_number = device_shot_numbers[0] if device_shot_numbers else None
        
        if unified_shot_number is None:
            log.error("Cannot determine shot number from master_data")
            return None
        
        # Step 3: Create instance and populate
        instance = cls(unified_shot_number)
        instance._parse_payload(master_data)
        instance._raw_master_data = master_data
        
        return instance
    
    # =========================================================================
    #               SHOT NUMBER EXTRACTION
    # =========================================================================
    
    @staticmethod
    def _collect_device_shot_numbers(master_data: dict) -> list[int]:
        """
        Extract shot numbers for devices from master_data structure.
        
        Returns a dictionary mapping device addresses to their shot numbers.
        """
        result = {}
        
        # Safely navigate to the payload data
        try:
            data = master_data.get('payload', {}).get('data', {}).get('results', {})
            log.info(f'results dict: {data}')
        except (AttributeError, TypeError):
            return result
        
        # Collect from outputs (most direct device-shot mapping)
        outputs = data.get('outputs', {})
        for device_id, output_data in outputs.items():
            if isinstance(output_data, dict) and 'shot_number' in output_data:
                result[device_id] = output_data['shot_number']
        
        # Collect from actuators (also has device shot numbers)
        actuators = data.get('actuators', {})
        for device_id, actuator_data in actuators.items():
            if isinstance(actuator_data, dict) and 'shot_number' in actuator_data:
                result[device_id] = actuator_data['shot_number']
        
        # Optionally include shot_number_from_diags if it exists
        diags_shots = data.get('shot_number_from_diags', {})
        for device_id, shot_num in diags_shots.items():
            if device_id not in result:  # Don't overwrite outputs/actuators
                result[device_id] = shot_num
        
        # Store the master-level shot number separately if needed
        if 'shot_number_from_master' in data:
            # This represents the overall shot number, not tied to a specific device
            result['_master'] = data['shot_number_from_master']
        
        return result
        
    @staticmethod
    def _verify_shot_congruence(shot_numbers: dict) -> tuple[int, bool]:
        """
        Check if all shot numbers match.
        Returns (shot number, True) if consistent, (shot number from master, True) if mismatched.
        """
        if not shot_numbers:
            return None

        prev_shotnum = None
        for shot_number in shot_numbers.values():
            if prev_shotnum is None:
                prev_shotnum = shot_number
            else:
                if shot_number == prev_shotnum:
                    continue
                else: 
                    return (shot_numbers['_master'], False)
        return (shot_numbers['_master'], True)



    
    # =========================================================================
    #                       PAYLOAD PARSING
    # =========================================================================
    
    def _parse_payload(self, master_data: dict) -> None:
        """Orchestrate parsing of payload structure."""
        results = self._extract_results(master_data)
        if results is None:
            return
        
        self._parse_actuators(results)
        self._parse_outputs(results)
    
    @staticmethod
    def _extract_results(master_data: dict) -> dict | None:
        """Extract the results section from master_data payload."""
        try:
            return master_data['payload']['data']['results']
        except KeyError as e:
            log.error(f"Cannot extract results: missing key {e}")
            return None
    
    def _parse_actuators(self, results: dict) -> None:
        """Parse actuator/motor information from results."""
        try:
            actuators = results['actuators']
            log.info(f"Found {len(actuators)} actuators")
            log.info(f'Actuator(s): {actuators}')
            
            for actuator in actuators:
                # Extract shot number per actuator for secondary verification
                #actuator_shot = actuator.get('shot_number')
                pass
                
                # TODO: Store motor data based on rack_address and index
                # self._store_motor(actuator)
                
        except KeyError:
            log.info("No actuators in results")
        except Exception as e:
            log.error(f"Error parsing actuators: {e}")
    
    def _parse_outputs(self, results: dict) -> None:
        """Parse diagnostic outputs from results."""
        try:
            diagnostics = results['outputs']
            log.info(f"Found {len(diagnostics)} diagnostics")
            
            # Process diagnostics as needed
            for name, data in diagnostics.items():
                # self._store_diagnostic(name, data)
                pass
                
        except KeyError:
            log.info("No outputs in results")
        except Exception as e:
            log.error(f"Error parsing outputs: {e}")